import json, os, sys, time, numpy as np, vmecpp
sys.path.insert(0, os.path.dirname(__file__)); from plasma_metrics import metrics
SRC = "evidence/plasma-balanced-v1/selected-input-401.json"; OUT = sys.argv[1]; T0 = time.time(); BUDGET = 7200
def solve(mods, tag):
    i = vmecpp.VmecInput.from_file(SRC)
    i.ns_array = np.array([12, 25, 51, 99]); i.ftol_array = np.array([1e-8, 1e-10, 1e-11, 1e-13]); i.niter_array = np.array([10000]*4)
    for (k, m, n), h in mods: getattr(i, k)[m, n+i.ntor] += h
    f = os.path.join(os.path.dirname(OUT), f"wout_{tag}.nc")
    try:
        o = vmecpp.run(i, max_threads=1, verbose=False); o.wout.save(f)
        r = metrics(f); r.update(ier=int(o.wout.ier_flag), volume=float(o.wout.volume_p))
    except Exception as e: r = dict(error=repr(e))
    if os.path.exists(f) and tag != "base": os.remove(f)
    return r
if __name__ == "__main__":
    i = vmecpp.VmecInput.from_file(SRC)
    modes = [(k, m, n-i.ntor) for k in ("rbc", "zbs") for m in range(i.mpol) for n in range(2*i.ntor+1)
             if getattr(i, k)[m, n] != 0 and not (k == "rbc" and m == 0 and n == i.ntor)]
    checks = [("rbc", 0, 1), ("rbc", 2, 0), ("zbs", 1, 1), ("zbs", 2, 0)]
    jobs = [("base", [], None, 0)] + [(f"{k}{m}_{n}", [((k, m, n), 1e-3)], (k, m, n), 1e-3) for k, m, n in modes] \
         + [(f"{k}{m}_{n}_h5e-4", [((k, m, n), 5e-4)], (k, m, n), 5e-4) for k, m, n in checks]
    with open(OUT, "a") as fh:
        for tag, mods, mode, h in jobs:
            if time.time()-T0 > BUDGET: fh.write(json.dumps(dict(stopped="budget"))+"\n"); break
            t = time.time(); r = solve(mods, tag)
            fh.write(json.dumps(dict(tag=tag, mode=mode, h=h, s=round(time.time()-t, 1), **r))+"\n"); fh.flush()
