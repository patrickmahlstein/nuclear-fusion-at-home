# N29 preregistration (#48): narrow-domain bounce action from realized-label-matched launches, reference401 fit

Follows N28 (s <= 0.75 qualifies; s = 0.9 cannot be matched). Inputs as N28 (snapshot ec1f8ce7..., Wout 0f2b626c).
Domain (fixed now): narrow, s in {0.25, 0.5, 0.75} x q in {0.1, 0.3, 0.5, 0.7, 0.9}; registered diagnostic
resolution nphi 801, nalpha 16, 2 periods; fusion_baselines.coil_bounce measure/trace_coils unchanged.
Matching: per alpha line, launch label sigma at the line's own target theta (phi = 0) root-found as in N28 so that
|s_real - s| <= 1e-3 (<= 5 traces). If any line on a surface is unmatched, that surface's matched result is
"incomplete" and no narrow score is formed.
Reported in the same run: ideal narrow score, coil narrow score from target launches (original convention),
coil narrow score from matched launches; per-cell scores and errors kept.
Selection/tolerance: descriptive only; no transfer claim (selected401 arm blocked on its original Wout).
Budget <= 1.5 h, one thread.
