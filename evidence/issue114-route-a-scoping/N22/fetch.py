"""Metric columns only from ConStellaration default parquet shards (revision 8da71572), remote column projection."""
import fsspec, pyarrow.parquet as pq, pyarrow as pa, sys, time
REV = "8da71572eb63ce93e77ce89bec0d7c30b7eba89e"
COLS = ["metrics.aspect_ratio", "metrics.flux_compression_in_regions_of_bad_curvature", "metrics.max_elongation",
        "metrics.edge_magnetic_mirror_ratio", "metrics.qi", "metrics.vacuum_well",
        "metrics.edge_rotational_transform_over_n_field_periods", "metrics.minimum_normalized_magnetic_gradient_scale_length",
        "boundary.n_field_periods"]
fs = fsspec.filesystem("https")
tables = []
for i in range(3):
    url = f"https://huggingface.co/datasets/proxima-fusion/constellaration/resolve/{REV}/data/train-0000{i}-of-00003.parquet"
    t = time.time()
    with fs.open(url, "rb", block_size=2**20, cache_type="readahead") as f:
        pf = pq.ParquetFile(f)
        names = pf.schema_arrow.names
        cols = [c for c in COLS if c in names]
        tables.append(pf.read(columns=cols))
    print(i, tables[-1].num_rows, round(time.time()-t, 1), flush=True)
pq.write_table(pa.concat_tables(tables), sys.argv[1])
