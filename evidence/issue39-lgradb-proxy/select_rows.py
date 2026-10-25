"""N45: apply the preregistered selection rule to ConStellaration rev 8da71572, then save each chosen row's boundary.
Usage: python select_rows.py OUTDIR"""
import json, math, sys
from pathlib import Path
import fsspec, numpy as np, pyarrow as pa, pyarrow.parquet as pq
REV = "8da71572eb63ce93e77ce89bec0d7c30b7eba89e"
M = ["aspect_ratio", "flux_compression_in_regions_of_bad_curvature", "max_elongation", "edge_magnetic_mirror_ratio",
     "qi", "vacuum_well", "edge_rotational_transform_over_n_field_periods", "minimum_normalized_magnetic_gradient_scale_length"]
COLS = [f"metrics.{m}" for m in M] + ["boundary.n_field_periods", "boundary.is_stellarator_symmetric"]
B = ["boundary.r_cos", "boundary.z_sin", "boundary.n_field_periods", "boundary.is_stellarator_symmetric", "metrics.id"]
TARGETS = [2.5, 3.5, 4.0, 5.0, 5.5, 6.5, 8.0, 9.0, 10.0, 11.0, 2.0, 3.0, 6.0, 7.0]  # amendment 1 appends four
USED = {60653, 2931, 46244, 23761}
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
fs = fsspec.filesystem("https")
urls = [f"https://huggingface.co/datasets/proxima-fusion/constellaration/resolve/{REV}/data/train-0000{i}-of-00003.parquet"
        for i in range(3)]
tabs, offsets = [], [0]
for u in urls:
    with fs.open(u, "rb", block_size=2**20, cache_type="readahead") as f:
        pf = pq.ParquetFile(f); names = pf.schema_arrow.names
        tabs.append(pf.read(columns=[c for c in COLS if c in names]))
    offsets.append(offsets[-1] + tabs[-1].num_rows)
t = pa.concat_tables(tabs, promote_options="default").to_pandas()
print("rows", len(t), "offsets", offsets, flush=True)
lgb = t["metrics.minimum_normalized_magnetic_gradient_scale_length"]
ok = ((t["boundary.n_field_periods"] == 2) & (t["boundary.is_stellarator_symmetric"] == True)
      & t["metrics.aspect_ratio"].between(9.5, 10.5) & (t["metrics.qi"] > 0) & (np.log10(t["metrics.qi"].where(t["metrics.qi"] > 0)) <= -2.5)
      & (t["metrics.edge_rotational_transform_over_n_field_periods"].abs() >= 0.15)
      & np.isfinite(t[[f"metrics.{m}" for m in M]]).all(axis=1) & ~t.index.isin(USED))
pool = t[ok]
print("eligible", len(pool), "L∇B range", float(pool[lgb.name].min()), float(pool[lgb.name].max()), flush=True)
chosen, report = set(), []
for target in TARGETS:
    d = (pool[lgb.name] - target).abs().drop(index=list(chosen), errors="ignore")
    row = int(d.sort_values(kind="stable").index[0]) if len(d) else None
    # ties -> lowest index: stable sort on an ascending index
    if row is None or d[row] > 0.3:
        report.append(dict(target=target, row=None, dropped=True)); continue
    chosen.add(row); report.append(dict(target=target, row=row, lgradb=float(pool.at[row, lgb.name])))
print(json.dumps(report), flush=True)
for r in report:
    if not r.get("row"): continue
    row = r["row"]; shard = max(i for i in range(3) if offsets[i] <= row); local = row - offsets[shard]
    with fs.open(urls[shard], "rb", block_size=2**20, cache_type="readahead") as f:
        pf = pq.ParquetFile(f); start = 0
        for g in range(pf.num_row_groups):
            n = pf.metadata.row_group(g).num_rows
            if local < start + n:
                rg = pf.read_row_group(g, columns=[c for c in B if c in pf.schema_arrow.names]).to_pylist()[local - start]; break
            start += n
    rec = dict(row=row, revision=REV, metrics_id=rg.get("metrics.id"),
               boundary=dict(r_cos=rg["boundary.r_cos"], z_sin=rg["boundary.z_sin"],
                             n_field_periods=rg["boundary.n_field_periods"],
                             is_stellarator_symmetric=rg["boundary.is_stellarator_symmetric"]),
               metrics={m: float(t.at[row, f"metrics.{m}"]) for m in M})
    (out/f"row{row}.json").write_text(json.dumps(rec))
(out/"selection.json").write_text(json.dumps(dict(eligible=int(len(pool)), report=report), indent=1))
# N33 rows' stored metrics, for the secondary proxies
(out/"n33-rows.json").write_text(json.dumps({r: {m: float(t.at[r, f"metrics.{m}"]) for m in M} for r in sorted(USED)}, indent=1))
