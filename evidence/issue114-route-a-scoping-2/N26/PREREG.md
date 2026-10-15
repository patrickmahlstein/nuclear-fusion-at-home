# N26 preregistration — DESC omnigenity pipeline with a vacuum-well term at nfp=2 (exploratory, #114)

Question: ConStellaration generated its QI-like dataset with a DESC omnigenity optimization. Its 7 nfp=2, A 9-11
rows with log10 QI <= -3.5 all have deep anti-wells (W -0.11..-0.15) and elongation 5.5-7.2. If the same
pipeline also gets MagneticWell >= 0 (weight 10) and Elongation <= 4.5 (FC proxy, from N22), does it produce an
nfp=2 boundary that meets the MHD-stable bounds (forward model, high fidelity)?
Seeds (fixed now): rows 31002 and 43213 (lowest FC among the 7: 1.001 and 0.933), ConStellaration default split
revision 8da71572 (MIT). Their stored targets (omnigenous field, A, elongation, iota) and DESC settings are used
unchanged (lsq-auglag, maxiter 200, M=N=4).
Arms per seed: ctrl (pipeline unchanged; checks we reproduce a QI-good boundary) and well (+ the two terms).
Run sequentially, one process, <= 1 h per run; total <= 4 h.
Outcome: per arm, MHD-stable normalized feasibility, all metrics. "nfp=2 design found" only if feasibility <= 1e-2
at A <= 10.5 (benchmark bound is a multi-objective A; we report A). Draft-v1 QI <= -4 checked separately.
