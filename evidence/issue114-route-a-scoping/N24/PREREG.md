# N24 preregistration — corrected selected401 arm of N23 (written before running, after N23 sel401 withdrawal)

Question: starting from selected401 (nfp=2, A~10), can ConStellaration's ALM-NGOpt reach MHD-stable feasibility
(normalized violation <= 1e-2; benchmark bounds) at A <= 10 within the N23 per-arm budget?
Changes vs N23 (both fixing seed-independent defects found in N23, see N23/DEVIATIONS.md):
- runner iota constraint uses |iota| (as the problem's own scoring does);
- max_toroidal_mode 6 (rule fixed before optimizing: smallest of {6,8,10} keeping high-fidelity log10 QI <= -4.0
  for the truncated seed; 6 gives -4.49, 8 gives -4.61; 4 gave -3.45).
Everything else as N23 (maxit 10, budget 800+100, 6 workers, very_low_fidelity, seed 123, 1.5 h wall).
Report: best normalized feasibility at A<=10, per-constraint values, L∇B; re-evaluate best at high fidelity;
check draft-v1's stricter QI <= -4 separately. Positive feasibility = existence at nfp=2 near our design.
Failure = "not found at this budget", not infeasible.
