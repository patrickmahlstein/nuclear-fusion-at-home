# Plasma requirements calibration evidence

Calibration input for issue #113, not owner approval or a frozen gate.
The protocol was committed before metric access (64ac4f2, schema clarification
 d516c1e). All paths below are relative to this directory.

## Reproduce

Use Python 3.14.8 with PyArrow 26.0.0 in a separate disposable environment.
`fetch_ranges.py` fetches only 692 manifest-bound ranges, totaling 21,510,090
input bytes. It requires 3 GiB initial / 2 GiB live disk reserve and permits
at most 128 MiB input transfer with a 15-minute transfer deadline. Raw range
inputs remain local and are obtainable from the pinned dataset; no full shard,
boundary payload, Wout or native environment is needed. Whole-shard published
LFS hashes are recorded in range-plan.json, not independently verified here.

```bash
python fetch_ranges.py
python calibrate.py --self-test
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 ARROW_NUM_THREADS=1 python calibrate.py replay.json
```

Expected replay bytes match calibration.json with the recorded Python/PyArrow
versions. Producer-base and source/data/range hashes are in provenance.json.
The analysis imports no fetched publisher code. Cache mutation fails checksum
validation before analysis. The original raw cache is retained outside Git.

`independent-probe.py` and `independent-result.json` record a second arithmetic
implementation, sharing the verified data reader and PyArrow. Replay it with:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 ARROW_NUM_THREADS=1 python independent-probe.py --output independent-replay.json
```

The wrapper now uses this directory by default, with explicit `--cache` and
`--output` options. This corrects the original snapshot's machine-specific paths;
its arithmetic is unchanged. Its QI minima/global count are explicitly
exploratory diagnostics after the zero selected-QI result, not changed calibration
subpopulations or thresholds. The original immutable tag/commit remains available;
this correction and the co-occurrence supplement receive a new tag.

## Scope and caveats

The pinned default dataset has 182,222 published rows; 23,537 lack selection
fields. The registered comparable subset contains 12,366 unique boundary IDs
with all five metrics finite. QI passes and therefore metric-only joint passes
are zero. Earlier generation flags often are null; forward-model flags are
false throughout this subset. Unknown flags never pass the primary joint check.
These are row-prevalence statistics, not independent-family feasibility odds.
Stored labels remain conditional on #112 producer/fidelity and scorer checks.
The owner must approve and freeze requirements separately. No physics admission,
optimization or requirement relaxation follows from this record.

Data attribution: Proxima Fusion; pinned Hugging Face dataset card declares MIT.
Only projected-column manifests and derived summaries are redistributed here.
