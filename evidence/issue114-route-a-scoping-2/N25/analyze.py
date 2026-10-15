"""N23: per arm, eval count, best normalized feasibility, feasible evals and best L∇B."""
import glob, json, os, sys
import constellaration.problems as problems
from constellaration.forward_model import ConstellarationMetrics
P = problems.MHDStableQIStellarator()
here = os.path.dirname(os.path.abspath(__file__))
for arm in sorted(d for d in os.listdir(here) if os.path.isdir(os.path.join(here, d)) and d.startswith(("row", "nae", "sel"))):
    rows = []
    for f in glob.glob(os.path.join(here, arm, "evals-*.jsonl")):
        for l in open(f):
            try: rows.append(json.loads(l))
            except ValueError: pass
    ok = [r for r in rows if "metrics" in r]
    if not rows: print(arm, "no evals"); continue
    best, feas = None, []
    for r in ok:
        m = ConstellarationMetrics(**r["metrics"])
        if m.aspect_ratio > 10.0: continue
        f = P.compute_feasibility(m)
        if best is None or f < best[0]: best = (f, m, r)
        if f <= 1e-2: feas.append((m.minimum_normalized_magnetic_gradient_scale_length, f, m.aspect_ratio))
    print(f"{arm}: evals {len(rows)} ok {len(ok)} A<=10 feasible(<=1e-2) {len(feas)}"
          + (f" best L∇B {max(feas)[0]:.2f}" if feas else ""))
    if best:
        f, m, r = best
        print(f"   least-violating (A<=10): feas {f:.4f} A {m.aspect_ratio:.2f} FC {m.flux_compression_in_regions_of_bad_curvature:.3f} "
              f"W {m.vacuum_well:.4f} log10QI {__import__('math').log10(m.qi):.2f} mirror {m.edge_magnetic_mirror_ratio:.3f} "
              f"iota/nfp {m.edge_rotational_transform_over_n_field_periods:.3f} elong {m.max_elongation:.2f} L∇B {m.minimum_normalized_magnetic_gradient_scale_length:.2f}")
        json.dump(r["boundary"], open(os.path.join(here, arm, "best-boundary.json"), "w"))
