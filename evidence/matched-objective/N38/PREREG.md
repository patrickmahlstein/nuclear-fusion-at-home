# N38 preregistration: fitter objective matched to acceptance v2's binding term (paired)

Observation (leaderboard-v2, selected401 v2 passes): boundary mean binds (ratios 0.76-0.82) while boundary max
(~0.6) and interior RMS (~0.17) have slack. The fitter minimizes SIMSOPT local squared flux (area-weighted L2 of
B.n/|B|); acceptance scores the plain per-point mean of |B.n|/|B|.
Change (code ace5eb4, opt-in): --flux-objective mean-abs = 0.5*m^2, m = mean_i sqrt(e_i^2 + 1e-8), e_i = B.n/|B| on
the 64x64 half-period search grid; gradient verified against finite differences (6e-9 at h = 1e-7).
Arms (run in parallel, one thread each, same machine state): identical #102-arm-A recipe
(--order 8 --margins halved --interior-weight 0.05 --seconds 1800 --check-seconds 900), selected401 via
--target-spec on the regenerated Wout (N18 spec, length-headroom seed); L = --flux-objective local (control),
M = --flux-objective mean-abs. Code for both arms: the N38 branch (default path byte-identical, 426 tests).
Primary outcome: worst v2 ratio (acceptance_v2.py) of each arm, continuous geometry must pass.
Rule: "objective helps" if M <= 0.95 * L (5% bar, as #109) and M passes v2; "no effect" if within +-5%;
"hurts" if M >= 1.05 * L. Report boundary mean/max, interior, geometry for both.
Not acceptance-of-record (regenerated-Wout target identity).
