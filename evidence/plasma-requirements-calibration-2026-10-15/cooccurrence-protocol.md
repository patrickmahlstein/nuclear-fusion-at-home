# Exploratory hard-bound co-occurrence diagnostic

Registered before co-occurrence counts, 2026-10-15T04:50:39.024644+00:00.
Primary calibration PR #119 remains unchanged and conditional on #112.

Decision: does the zero joint-pass result arise only from the QI threshold, or
do the other proposed exact bounds also lack a shared comparable population?
This informs owner review of attainable requirements and the future repair task.
It neither adopts nor relaxes any requirement or selects an optimization seed.

Inputs: the same manifest-verified projected ranges at dataset revision
8da71572eb63ce93e77ce89bec0d7c30b7eba89e; primary script SHA-256
25e96145b76b860961b8a6e0a2e4ad6e047d498a08321a2da741c5a23a30316f.
Selection stays nfp=2 and aspect ratio in closed [9,11]. Reuse all five exact
inequalities, the absolute-transform convention and primary missingness rules.

Compute every one of the 32 full pass/fail masks over the five original bounds,
all pairwise intersections and all original-bound subset intersections. Report
all counts rather than choosing favorable subsets. Metric-only co-occurrence
is a diagnostic, never admission with omitted constraints. Keep invalid metrics
separate; none are expected from the primary result. Report flag completeness
separately. Do not recompute native metrics, adjust thresholds, widen population,
rank or select boundaries, or infer independent-family feasibility odds.

Use a separate short arithmetic implementation and cross-check its marginals
and all-five count against frozen calibration.json. One offline pass, one thread,
three-minute ceiling, no downloads, at most 1 MiB generated output and 3/2 GiB
initial/live disk reserve. Retain failures. Publish a substantive supplementary
comment only if it changes the owner decision; otherwise record no added value.
