# N23 preregistration — can ConStellaration's own ALM-NGOpt find an nfp=2 MHD-stable QI design at A<=10?

Decision: informs owner's design-class choice for #113/#114 (nfp=2 vs nfp=3). Exploratory; benchmark bounds
(MHDStableQIStellarator defaults: log10 QI<=-3.5, mirror<=0.25, FC<=0.9, W>=0, iota/nfp>=0.25), A<=10.
Env: micromamba scratch env, constellaration 0.2.6, vmecpp 0.4.11, simsopt 1.8.1, booz_xform 0.1.0 (conda-forge;
pinned 0.0.9 failed to build). Control: reproduces #76 metrics for both targets to all recorded digits.
Settings: their launch_alm_mhd_stable_stellarator.py except maxit 10 (was 50), budget_initial 800 (1500),
increment 100 (300), num_workers 6 (48); very_low_fidelity; modes 4/4; seed 123.
Arms (sequential, equal settings): nae3 (their published seed, control), nae2 (same recipe nfp=2),
sel401 (selected401 input, truncated to 4/4 by the runner).
Logged: every evaluation (objective, constraints, metrics, boundary).
Outcome per arm: best normalized feasibility; count of evals with all constraints <= 0 and their best L∇B, A.
Then re-evaluate each arm's best feasible (or least-violating) boundary at default high fidelity.
Interpretation rule: if nae3 reaches feasibility (<=1e-2 normalized) and nae2/sel401 do not, report
"nfp=2 harder at equal budget", not infeasible. If nae3 fails too, report inconclusive (budget too small).
Budget: <=1.5 h wall per arm, <=1 GiB logs.
