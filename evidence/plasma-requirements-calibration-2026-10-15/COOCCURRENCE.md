# Exploratory exact-bound co-occurrence

Question: does primary zero joint prevalence reflect only QI, or do the other
proposed bounds also lack a shared comparable population? This is owner input,
not an alternative admission rule or a threshold change.

Protocol: cooccurrence-protocol.md, fixed before these counts but after primary
PR #119. Inputs and all original bounds/population remain unchanged. The script
reports all 32 exact masks and all subset intersections, preserving zeros and
missingness. Only offline verified ranges were used; no new downloads, native
computation, boundary selection or requirement changes.

## Result

Among the same 12,366 unique nfp=2, aspect-ratio 9–11 rows, ten meet the four
non-QI bounds together (0.08087%). This subset is diagnostic and does not pass
proposed v1. All five together still have zero metric-only passes. QI therefore
is not the only attainability concern: even the other four have a rare shared
population under the exact proposed bounds.

| Diagnostic intersection | Rows |
| --- | ---: |
| Well and compression | 475 |
| Well and absolute transform | 26 |
| Well and mirror | 30 |
| Compression and absolute transform | 124 |
| Compression and mirror | 111 |
| Absolute transform and mirror | 927 |
| All four non-QI bounds | 10 |
| All five original bounds | 0 |

No selected row has all five historical generation/forward error flags known;
individual pipeline flags often are null. Thus the primary protocol's strict
all-flags-known joint count is conservative and would be zero independently of
metrics. The separately reported metric-only count is also zero because QI has
no passes; the primary scientific observation does not rely on flag semantics.
Do not treat non-applicable generation stages as demonstrated failures, or
silently change the original missingness rule after seeing outcomes.

## Reproduce and limits

From this evidence directory, after original fetch_ranges.py:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 ARROW_NUM_THREADS=1 python cooccurrence.py . replay-cooccurrence.json
```

The script SHA-256 is recorded in cooccurrence.json. Histogram-derived and direct
subset accumulations agree for all 32 subsets; primary marginals and all-five
count reproduce. This is a shared-reader arithmetic check, not independent
physics validation. Python 3.14.8, PyArrow 26.0.0; no new metric evaluations.

Producer/fidelity comparability remains conditional on #112. Selection bias and
unknown ancestry prohibit general feasibility probabilities. No conclusion is
made about whether optimizing near our plasma can meet v1. Owner approval and
freeze remain required before optimization.
