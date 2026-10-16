"""Dataset boundary -> VMEC++ input JSON using the selected401 input as template (schedule, phiedge, resolution).
The poloidal orientation is matched to the template's (theta -> -theta flip if the phi=0 section winds the other way),
because VMEC++ re-orients a boundary internally and its Wout then no longer equals the input coefficients."""
import json, math, sys
import numpy as np
tpl = json.load(open("evidence/plasma-balanced-v1/selected-input-401.json"))
rec = json.load(open(sys.argv[1])); b = rec["boundary"]; assert b["n_field_periods"] == 2 and b["is_stellarator_symmetric"]
rc, zs = np.array(b["r_cos"]), np.array(b["z_sin"]); nt = (rc.shape[1]-1)//2

def winding(rows_r, rows_z):  # signed area of the phi=0 section, theta increasing
    th = np.linspace(0, 2*math.pi, 400, endpoint=False)
    R = sum(v*np.cos(m*th) for m, n, v in rows_r); Z = sum(v*np.sin(m*th) for m, n, v in rows_z)
    return np.sign(np.sum(R*np.roll(Z, -1) - np.roll(R, -1)*Z))
ref = winding([(r["m"], r["n"], r["value"]) for r in tpl["rbc"]], [(r["m"], r["n"], r["value"]) for r in tpl["zbs"]])
rows = lambda a: [(m, n-nt, a[m, n]) for m in range(a.shape[0]) for n in range(a.shape[1])]
flip = winding(rows(rc), rows(zs)) != ref
if flip:  # theta -> -theta: cos(m t - n N p) -> cos(m t + n N p) => rbc(m,n) -> rbc(m,-n); zbs(m,n) -> -zbs(m,-n)
    rc, zs = rc[:, ::-1].copy(), -zs[:, ::-1].copy()
    rc[0], zs[0] = np.array(b["r_cos"])[0], np.array(b["z_sin"])[0]  # m = 0 terms do not depend on theta
tpl["rbc"] = [dict(m=m, n=n-nt, value=float(rc[m, n])) for m in range(rc.shape[0]) for n in range(rc.shape[1])
              if rc[m, n] != 0 and not (m == 0 and n < nt)]
tpl["zbs"] = [dict(m=m, n=n-nt, value=float(zs[m, n])) for m in range(zs.shape[0]) for n in range(zs.shape[1])
              if zs[m, n] != 0 and not (m == 0 and n <= nt)]
for k in ("raxis_c", "zaxis_s"):
    if k in tpl: tpl[k] = [float(rc[0, nt]) if (k == "raxis_c" and i == 0) else 0.0 for i in range(len(tpl[k]))]
json.dump(tpl, open(sys.argv[2], "w"), indent=1)
json.dump(dict(orientation_flipped=bool(flip)), open(sys.argv[2] + ".flip.json", "w"))
print("flipped", bool(flip))
