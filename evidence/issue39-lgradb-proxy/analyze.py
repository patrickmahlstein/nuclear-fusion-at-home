"""N45 analysis: per-plasma v2 metrics (acceptance_v2.py) + N33 rows as recorded; Spearman rho vs proxies.
Usage (worktree root): python analyze.py RESULTS_DIR OUT.json"""
import json, subprocess, sys, os
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
res = Path(sys.argv[1]); rows = res/"rows"
M = json.loads((rows/"n33-rows.json").read_text())
sel = json.loads((rows/"selection.json").read_text())["report"]
SEL401 = dict(minimum_normalized_magnetic_gradient_scale_length=6.14, max_elongation=5.96, qi=10**-4.66,
              edge_magnetic_mirror_ratio=0.235, flux_compression_in_regions_of_bad_curvature=1.398, vacuum_well=-0.0158,
              edge_rotational_transform_over_n_field_periods=0.2508)  # #76 / #113 table values
# N33 recorded outcomes (posted on #114): worse-shift boundary mean, max, interior RMS, geometry
N33 = {"60653": (0.00665, 0.0735, 0.0367), "2931": (0.00424, 0.0312, 0.0230), "sel401": (0.00161, 0.0091, 0.0103),
       "46244": (0.00305, 0.0158, 0.0061), "23761": (0.00311, 0.0307, 0.0179)}
table = []
for tag, (mean, mx, interior) in N33.items():
    met = SEL401 if tag == "sel401" else M[tag]
    table.append(dict(plasma=tag, source="N33", mean=mean, max=mx, interior=interior, geometry=True, **met))
for r in sel:
    if not r.get("row"): continue
    tag = str(r["row"]); fit = res/f"fit-{tag}"
    out = subprocess.run([sys.executable, "scripts/acceptance_v2.py", str(fit)], capture_output=True, text=True,
                         env={**os.environ, "PYTHONPATH": "src"})
    met = json.loads((rows/f"row{tag}.json").read_text())["metrics"]
    if out.returncode:
        table.append(dict(plasma=tag, source="N45", mean=None, error=out.stderr[-300:], **met)); continue
    a = json.loads(out.stdout)[0]
    table.append(dict(plasma=tag, source="N45", mean=max(b["mean"] for b in a["boundary"]),
                      max=max(b["max"] for b in a["boundary"]), interior=max(a["interior_vector_rms"]),
                      geometry=a["shared_checks"]["continuous_geometry"], v2=a["v2"]["passed"], **met))
worst = max(t["mean"] for t in table if t["mean"] is not None)
y = np.array([t["mean"] if t["mean"] is not None else 10*worst for t in table])  # no eligible candidate -> worst
proxies = {"L∇B": "minimum_normalized_magnetic_gradient_scale_length", "max elongation": "max_elongation",
           "log10 QI": "qi", "edge mirror": "edge_magnetic_mirror_ratio",
           "flux compression": "flux_compression_in_regions_of_bad_curvature", "vacuum well": "vacuum_well",
           "|iota|/nfp": "edge_rotational_transform_over_n_field_periods"}
rho = {}
for name, k in proxies.items():
    x = np.array([abs(t[k]) if "iota" in k else (np.log10(t[k]) if k == "qi" else t[k]) for t in table])
    rho[name] = float(spearmanr(x, y).statistic)
n = len(table); crit = {11: -0.536, 12: -0.503, 13: -0.484, 14: -0.464, 15: -0.45}[n]
p = rho["L∇B"]
verdict = "supports" if p <= crit else ("contradicts" if p >= 0 else "inconclusive")
report = dict(n=n, threshold=crit, rho=rho, primary=p, verdict=verdict, usable=abs(p) >= 0.7, table=table)
Path(sys.argv[2]).write_text(json.dumps(report, indent=1))
print(json.dumps({k: v for k, v in report.items() if k != "table"}, indent=1))
for t in sorted(table, key=lambda t: t["minimum_normalized_magnetic_gradient_scale_length"]):
    print(f'{t["plasma"]:>7} {t["source"]} L∇B {t["minimum_normalized_magnetic_gradient_scale_length"]:.2f} '
          f'elong {t["max_elongation"]:.2f} mean {t["mean"]:.5f} max {t["max"]:.4f} int {t["interior"]:.4f} geom {t.get("geometry")}')
