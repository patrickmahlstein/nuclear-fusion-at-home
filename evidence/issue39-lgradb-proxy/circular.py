"""Neutral seed: 6 planar circular coils of radius r, each centred on the plasma's phi-section centre (m=0 boundary
terms) at its toroidal angle, equally spaced in the half period. Usage: circular.py INPUT.json r OUT.json"""
import json, math, sys
d = json.load(open(sys.argv[1])); r = float(sys.argv[2]); nfp = d["nfp"]
tpl = json.load(open("submissions/length-headroom-six-coil/candidate.json"))
r0 = {row["n"]: row["value"] for row in d["rbc"] if row["m"] == 0}
z0 = {row["n"]: row["value"] for row in d["zbs"] if row["m"] == 0}
base = []
for i in range(6):
    p = (i + 0.5) * (math.pi / nfp) / 6
    Rc = sum(v*math.cos(-n*nfp*p) for n, v in r0.items()); Zc = sum(v*math.sin(-n*nfp*p) for n, v in z0.items())
    x = [0.0]*11; y = [0.0]*11; z = [0.0]*11
    x[0], x[2] = Rc*math.cos(p), r*math.cos(p)
    y[0], y[2] = Rc*math.sin(p), r*math.sin(p)
    z[0], z[1] = Zc, r
    base.append([x, y, z])
tpl["base_coefficients"] = base
json.dump(tpl, open(sys.argv[3], "w"))
