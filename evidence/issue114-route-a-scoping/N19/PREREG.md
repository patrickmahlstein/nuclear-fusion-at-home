# N19 preregistration (exploratory scoping for #114 stage 1, route A) — 2026-10-15 ~05:20Z

Question: which boundary modes of selected401 move vacuum well (W) and flux compression (FC)
of the native ConStellaration-0.2.6 mirror, and does a linear step that holds aspect ratio
and edge iota fixed reach W >= 0 and FC <= 0.9?
Base: evidence/plasma-balanced-v1/selected-input-401.json (6bec3483...), schedule ns 12/25/51/99,
ftol 1e-8/1e-10/1e-11/1e-13, niter 10000, cold start, vmecpp 0.8.0, simsopt 1.11.1, one thread.
Mirror: W from gmnc (linear extrapolation axis/LCFS); FC at s=0.49, 101 lines, 64 points.
Base check (done before preregistration): ns99 W -0.015768, FC 1.38735; ns401 W -0.015757, FC 1.38486.
FD: one-sided h=1e-3 on every nonzero rbc/zbs except rbc(0,0); record W, FC, aspect, iota_edge/nfp,
volume, ier_flag. Step check: h=5e-4 on rbc(0,1), rbc(2,0), zbs(1,1), zbs(2,0); linearity flagged if
the two slopes differ by >20%.
Analysis: least-norm boundary step dx solving J_{W,FC,A,iota} dx = (0.016+0.005, 0.9-FC0-0.05, 0, 0)
(margins 0.005 and 0.05 fixed now); then ONE nonlinear verification solve at dx, dx/2 and 2dx (ns99), mirror only.
Outcome rule: "linear route plausible" only if the dx solve has W>=0, FC<=0.9, |dA|<0.1, iota/nfp>=0.25.
Else report the achieved fractions. No claim of v1 feasibility; ConStellaration scorer of record is #112.
Budget: 2 h wall, 2 GiB disk, stop on budget and keep partial jsonl.
