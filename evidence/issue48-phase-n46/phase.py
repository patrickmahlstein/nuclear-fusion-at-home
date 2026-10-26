"""N46 (#48): s = 0.5 phase consistency with a construction-free (straight-field-line) ordering.
Usage (repo root): python phase.py SNAPSHOT WOUT QUAL.json OUT.json"""
import json, math, sys, time
import numpy as np
sys.path.insert(0, "src")
from fusion_baselines import realized_field as rf
from scipy.interpolate import CubicSpline
from simsopt.field import BiotSavart
from simsopt.field.tracing import compute_fieldlines

snap = json.load(open(sys.argv[1])); target = rf.Target.from_wout(sys.argv[2]); qual = json.load(open(sys.argv[3]))
field = BiotSavart(rf.coils(dict(parameter_names=snap["names"], base_coefficients=snap["base_coefficients"]), 1e5*snap["scale"]))
axis = np.array(qual["axis"]); t0 = time.monotonic()

def rz(sigma, th):  # identical to N28
    x = sigma*(target.ns-1); j = min(int(x), target.ns-2); w = x-j
    rm = (1-w)*target.rmnc[j]+w*target.rmnc[j+1]; zm = (1-w)*target.zmns[j]+w*target.zmns[j+1]
    a = th*target.xm
    return float(np.sum(rm*np.cos(a))), float(np.sum(zm*np.sin(a)))

def trace(starts, transits, tol):  # identical to N28
    r0 = [s[0] for s in starts]; z0 = [s[1] for s in starts]
    _, hits = compute_fieldlines(field, r0, z0, tmax=1.3*transits*2*math.pi*max(r0), tol=tol, phis=[0.0], stopping_criteria=[])
    return [np.column_stack((np.hypot(h[:, 2], h[:, 3]), h[:, 4]))[h[:, 1] == 0] for h in hits]

def spline_curve(p):  # N28 construction: geometric-angle ordering, periodic cubic spline in arc length
    psi = np.arctan2(p[:, 1]-axis[1], p[:, 0]-axis[0]); o = np.argsort(psi)
    c = np.vstack((p[o], p[o][:1])); t = np.concatenate(([0.0], np.cumsum(np.hypot(*np.diff(c, axis=0).T))))
    sp = CubicSpline(t, c, bc_type="periodic"); return sp(np.linspace(0, t[-1], 4000, endpoint=False))

def rotation(p):
    psi = np.unwrap(np.arctan2(p[:, 1]-axis[1], p[:, 0]-axis[0])); return (psi[-1]-psi[0])/(2*math.pi*(len(p)-1))

def polyline(p, iota):  # straight-field-line ordering
    o = np.argsort(np.mod(np.arange(len(p))*iota, 1.0)); c = p[o]; return c, np.roll(c, -1, axis=0)

def seg_dist(x, a, b):
    ab = b-a; t = np.clip(np.einsum("ij,kij->ki", ab, x[:, None, :]-a[None]) / np.maximum(np.sum(ab*ab, 1), 1e-300), 0, 1)
    proj = a[None]+t[..., None]*ab[None]; return np.min(np.hypot(*(x[:, None, :]-proj).transpose(2, 0, 1)), axis=1)

def nn(x, q): return np.min(np.hypot(*(x[:, None, :]-q[None]).transpose(2, 0, 1)), axis=1)

res = dict(levels={})
for s in (0.5, 0.75):
    cases = [c for c in qual["cases"] if c["s"] == s]
    starts = [rz(c["sigma"], c["theta"]) for c in cases]
    p60 = trace(starts, 60, 1e-10); p240 = trace(starts, 240, 1e-11)
    A = max(float(np.max(nn(p60[b], spline_curve(p60[a])))) for a in range(4) for b in range(4) if a != b)
    rot = [rotation(p) for p in p240]
    B = max(float(np.max(seg_dist(p240[b], *polyline(p240[a], rot[a])))) for a in range(4) for b in range(4) if a != b)
    A240 = max(float(np.max(nn(p240[b], spline_curve(p240[a])))) for a in range(4) for b in range(4) if a != b)
    res["levels"][str(s)] = dict(A_mm_60=1e3*A, A_mm_240=1e3*A240, B_mm_240=1e3*B, rotation=rot,
                                 rotation_spread=max(rot)-min(rot), crossings=[len(p) for p in p240])
    np.savez_compressed(f"{sys.argv[4]}.s{s}.npz", *p240)
    print(s, json.dumps(res["levels"][str(s)]), round(time.monotonic()-t0), flush=True)
L5, L75 = res["levels"]["0.5"], res["levels"]["0.75"]
res["control_A_reproduced"] = abs(L5["A_mm_60"]-1.697) <= 0.1
if L5["B_mm_240"] <= 1 and L75["B_mm_240"] <= 1 and L5["rotation_spread"] <= 1e-4: v = "artifact"
elif L5["B_mm_240"] > 1 and L75["B_mm_240"] <= 1: v = "real"
else: v = "unresolved"
res.update(verdict=v, seconds=time.monotonic()-t0)
json.dump(res, open(sys.argv[4], "w"), indent=1); print(v, res["control_A_reproduced"])
