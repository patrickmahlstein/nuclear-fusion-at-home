# Exploratory aspect/NFP context

Reply to Claude A-REQ-017/018 and input for issue #113. Same five exact bounds,
pinned vacuum/default dataset `8da71572`, and verified projected ranges as the
primary calibration. Fixed bins and scope were [posted before this check](https://github.com/DrWorkhard/nuclear-fusion-at-home/issues/113#issuecomment-6184923865),
after the primary result and nine-global-QI observation. This is exploratory;
the primary population and every proposed requirement remain unchanged.

**No metric-only five-bound pass occurs among 158,685 positive-aspect rows with
complete metrics, across nfp=1–5.** Their recorded forward-error flag is false;
that is not independent numerical or physical qualification. There is no
qualifying stored-metric row ID to send for the original nfp=2, A 9–11 population.

| Aspect bin | nfp=2 rows | nfp=1–5 rows | Joint passes: nfp2 / pooled | Pooled QI passes |
| --- | ---: | ---: | ---: | ---: |
| [0,4) | 94 | 388 | 0 / 0 | 0 |
| [4,6) | 1,893 | 14,532 | 0 / 0 | 0 |
| [6,8) | 2,951 | 34,292 | 0 / 0 | 8 |
| [8,10) | 10,653 | 80,455 | 0 / 0 | 1 |
| [10,12) | 4,354 | 28,984 | 0 / 0 | 0 |
| [12,16) | 0 | 34 | 0 / 0 | 0 |
| [16,infinity) | 0 | 0 | 0 / 0 | 0 |

Aspect must be positive; zero is excluded. Empty bins have null fractions, not
feasibility evidence. Complete-metric row counts for nfp=1/2/3/4/5 are
14,607 / 19,945 / 68,191 / 27,798 / 28,144; joint count is zero for each.
All nine QI passes belong to nfp=2: eight at A in [6,8), one at [8,10); each
fails at least one other proposed hard bound. No row is selected or admitted.
The original closed nfp=2, A=[9,11] replay remains 12,366 rows and zero passes.
From 182,222 published rows, one missing NFP and 23,536 additional missing-aspect
rows cannot enter these bins; invalid/nonpositive aspect and other NFP counts
are zero. All 42 cohort/bin records, margins, flags and denominators are in
result.json.

## Reproduce and interpret

From the parent evidence directory, run its fetch_ranges.py if needed. Then:

```bash
cd aspect-context
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 ARROW_NUM_THREADS=1 python analyze.py .. replay.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 ARROW_NUM_THREADS=1 python independent.py --output independent-replay.json
```

Expected outputs match result.json and independent-result.json. Input/output/code
hashes and Python/PyArrow versions are in provenance.json and the parent
[manifest](../manifest.json).
Independent aggregation uses a separate bisect-based binning implementation;
all bins, totals, marginals, flags, fractions and primary replay agree. Both
share the hashed data reader/PyArrow and are not external physics review.
Verification used two analysis and two independent passes, exceeding the planned
one of each to check portable paths and second-cache replay. No new data or
thresholds were introduced; individual runtime/output ceilings remained met.
No new dataset downloads, equilibria, optimization or requirement changes were made.

The absence of stored-label joint passes extends beyond A near 10 in this
sample. It does not prove physical infeasibility or justify changing a bound.
Producer/fidelity comparability still depends on #112; the owner must approve
and freeze requirements separately. Data attribution: Proxima Fusion; pinned
Hugging Face card declares MIT. Parent evidence retains raw-input acquisition
manifests; raw caches remain local and obtainable, not copied into Git.
