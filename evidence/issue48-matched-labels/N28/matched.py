"""N28 (#48): surface-matched launches on the #35 reference401 fit. Usage: python matched.py SNAPSHOT WOUT OUT.json
Reuses N9's direct-field flux-label construction (periodic spline through phi=0 crossings, Phi = loop A.dl)."""
import json, math, sys, time
import numpy as np
sys.path.insert(0, "src")
from fusion_baselines import realized_field as rf
from scipy.interpolate import CubicSpline
from simsopt.field import BiotSavart
from simsopt.field.tracing import compute_fieldlines

S_T = (0.1, 0.25, 0.5, 0.75, 0.9); THETAS = (0.0, math.pi/2, math.pi, 1.5*math.pi); NQ = 1024
snap = json.load(open(sys.argv[1])); target = rf.Target.from_wout(sys.argv[2]); OUT = sys.argv[3]
field = BiotSavart(rf.coils(dict(parameter_names=snap["names"], base_coefficients=snap["base_coefficients"]), 1e5*snap["scale"]))
t0 = time.monotonic()

def rz(sigma, th):  # target position at continuous label sigma (linear in s between full-grid surfaces)
    x = sigma*(target.ns-1); j = min(int(x), target.ns-2); w = x-j
    rm = (1-w)*target.rmnc[j]+w*target.rmnc[j+1]; zm = (1-w)*target.zmns[j]+w*target.zmns[j+1]
    a = th*target.xm
    return float(np.sum(rm*np.cos(a))), float(np.sum(zm*np.sin(a)))

def loop_flux(r, z, dr, dz):
    field.set_points(np.column_stack((r, np.zeros_like(r), z))); a = field.A()
    return float(np.mean(a[:, 0]*dr + a[:, 2]*dz)*2*math.pi)

def curve(rz_pts, centre):
    psi = np.arctan2(rz_pts[:, 1]-centre[1], rz_pts[:, 0]-centre[0]); o = np.argsort(psi)
    closed = np.vstack((rz_pts[o], rz_pts[o][:1])); t = np.concatenate(([0.0], np.cumsum(np.hypot(*np.diff(closed, axis=0).T))))
    star = bool(np.all(np.diff(np.unwrap(psi[o])) >= 0))
    return CubicSpline(t, closed, bc_type="periodic"), t[-1], star

def flux_of(rz_pts, centre):
    sp, L, star = curve(rz_pts, centre); q = np.linspace(0, L, NQ, endpoint=False); xy, d = sp(q), sp(q, 1); sc = L/(2*math.pi)
    return loop_flux(xy[:, 0], xy[:, 1], d[:, 0]*sc, d[:, 1]*sc), star

u = 2*math.pi*np.arange(NQ)/NQ; j = target.ns-1; ang = np.multiply.outer(u, target.xm)
flux_edge = loop_flux(np.sum(target.rmnc[j]*np.cos(ang), -1), np.sum(target.zmns[j]*np.sin(ang), -1),
                      np.sum(-target.xm*target.rmnc[j]*np.sin(ang), -1), np.sum(target.xm*target.zmns[j]*np.cos(ang), -1))

def trace(starts, transits, tol):
    r0 = [s[0] for s in starts]; z0 = [s[1] for s in starts]
    _, hits = compute_fieldlines(field, r0, z0, tmax=1.3*transits*2*math.pi*max(r0), tol=tol, phis=[0.0], stopping_criteria=[])
    return [np.column_stack((np.hypot(h[:, 2], h[:, 3]), h[:, 4]))[h[:, 1] == 0] for h in hits]

axis = trace([rz(0.005, 0.0)], 60, 1e-10)[0].mean(axis=0)
def labels(sigmas, transits=60, tol=1e-10):
    pts = trace([rz(sg, th) for sg, (s, th) in zip(sigmas, cases)], transits, tol)
    out = [flux_of(p, axis) for p in pts]
    return [f/flux_edge for f, _ in out], [st for _, st in out], pts

cases = [(s, th) for s in S_T for th in THETAS]
sig = [s for s, _ in cases]; hist = []
sr, star, _ = labels(sig); hist.append(dict(sigma=list(sig), s_real=sr, star=star))
prev_sig, prev_sr = list(sig), sr
sig = [sg + (s - r) for sg, (s, _), r in zip(sig, cases, sr)]
for it in range(4):
    sr, star, pts = labels(sig); hist.append(dict(sigma=list(sig), s_real=sr, star=star))
    if all(abs(r-s) <= 1e-3 for r, (s, _) in zip(sr, cases)): break
    new = []
    for i, (s, _) in enumerate(cases):
        d = sr[i]-prev_sr[i]; new.append(sig[i] + (s-sr[i])*((sig[i]-prev_sig[i])/d if abs(d) > 1e-12 else 1.0))
    prev_sig, prev_sr, sig = list(sig), sr, [min(max(x, 1e-3), 0.999) for x in new]
matched = [abs(r-s) <= 1e-3 for r, (s, _) in zip(sr, cases)]
# phase consistency: distance of each line's crossings to the spline of the other phases at the same s
phase = []
for k, s in enumerate(S_T):
    idx = [i for i, (ss, _) in enumerate(cases) if ss == s]; worst = 0.0
    for a in idx:
        sp, L, _ = curve(pts[a], axis); q = sp(np.linspace(0, L, 4000, endpoint=False))
        for b in idx:
            if a != b: worst = max(worst, float(np.max(np.min(np.hypot(*(pts[b][:, None, :]-q[None, :, :]).transpose(2, 0, 1)), axis=1))))
    phase.append(dict(s=s, max_cross_distance_mm=1e3*worst))
sr120, _, _ = labels(sig, 120, 1e-10); sr11, _, _ = labels(sig, 60, 1e-11)
res = dict(flux_edge=flux_edge, C1_rel=abs(flux_edge/(-math.pi/100)-1), axis=axis.tolist(), iterations=hist,
           cases=[dict(s=s, theta=th, sigma=sg, s_real=r, matched=m, star=st, s_real_120=a, s_real_tol11=b)
                  for (s, th), sg, r, m, st, a, b in zip(cases, sig, sr, matched, star, sr120, sr11)],
           phase=phase, seconds=time.monotonic()-t0)
json.dump(res, open(OUT, "w"), indent=1)
for c in res["cases"]: print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in c.items()}))
print(json.dumps(phase)); print("C1", res["C1_rel"], "seconds", round(res["seconds"]))
