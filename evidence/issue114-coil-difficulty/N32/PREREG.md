# N32 preregistration (#114 stage-2 hypothesis, exploratory): does higher L∇B make coil fitting easier?

Plasmas (fixed now): MIT dataset default 8da71572 nfp=2 rows with A 9.5-10.5, log10 QI <= -2.5, |iota|/nfp >= 0.15,
nearest to L∇B 3 / 4.5 / 7 / 8.5: rows 60653 (3.00), 2931 (4.50), 46244 (6.99), 23761 (7.41); plus selected401
(6.14, regenerated Wout 3d5df9a4, spec selected401-regen-vmecpp080).
Intake: boundary -> VMEC++ input (selected401 template: schedule to ns 401, phiedge, mpol 5/ntor 10; axis guess
reset) -> make_wout.py -> make_target_spec.py (seed: public length-headroom candidate, retargeted).
Fit recipe (identical): fit_coils.py --seconds 1800 --check-seconds 900, current margins, order 5, no interior term.
Primary outcome: Spearman rho between L∇B (stored dataset value; #76 value for selected401) and fine boundary
mean (acceptance_v2 'mean', worse of the two shifts). Hypothesis: rho < 0. With n = 5, report rho; "supports"
only if rho <= -0.9 (one-sided 5% critical value), "contradicts" if rho >= 0, else "inconclusive".
Secondary: boundary max, interior RMS, geometry status, v2 verdict per plasma; max elongation as alternative proxy.
Failures (Wout/spec/fit) are kept and reported, not replaced. Different targets' errors are not acceptance-comparable;
this is a difficulty proxy test only. Budget: <= 5 h, one thread, <= 2 GiB.
