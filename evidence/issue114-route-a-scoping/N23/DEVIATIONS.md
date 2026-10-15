11:25Z first launch crashed (forkserver bootstrap: missing __main__ guard). Wrapped in main(); logic unchanged. Relaunched.
~12:55Z nae3 reached 5400 s wall budget and was stopped; launcher then crashed on second killpg (EPERM on exited group) before nae2. Launcher fixed (try/except, arm list arg); nae2 and sel401 launched afterwards with identical settings. Load from other processes may differ between arms (wall budget, not eval budget).
~13:10Z sel401 arm withdrawn before start. Reasons found after nae3 (documented, not outcome-driven for sel401):
(1) constellaration 0.2.6 augmented_lagrangian_runner.objective_constraints uses signed iota
    (bound - iota) while MHDStableQIStellarator._normalized_constraint_violations uses |iota|; selected401
    has iota/nfp = -0.25, so the runner treats it as violated by 0.5 and pushes iota through zero.
(2) runner truncation to modes 4/4 raises selected401 log10 QI from -4.62 to -3.48 (high fidelity -3.45).
nae3/nae2 seeds start at iota ~0 (nae3 first -0.007, nae2 first -0.02), so they remain comparable to each other.
A corrected selected401 arm goes to a separate preregistration (N24).
