# N45 preregistration (#39 / #114 stage 2, exploratory): is L∇B a usable coil-difficulty proxy? (N33 at n = 15)

Decision served: #116's planned joint optimizer (#39) uses "an outer plasma loop with cheap coil-difficulty proxies".
N33 (n = 5) gave Spearman rho(L∇B, fitted boundary mean) = -0.6, inconclusive. This extends the same test to n = 15.

Plasmas (selection rule fixed now, before any data is looked at for this run):
- ConStellaration dataset, default config, revision 8da71572eb63ce93e77ce89bec0d7c30b7eba89e (MIT licence), global
  row index = concatenation order of train-00000..00002 (as N22/N32).
- Eligible: nfp 2, stellarator-symmetric, aspect 9.5-10.5, log10 QI <= -2.5, |iota_edge|/nfp >= 0.15, all metrics finite,
  not one of N33's rows (60653, 2931, 46244, 23761).
- Targets L∇B = 2.5, 3.5, 4.0, 5.0, 5.5, 6.5, 8.0, 9.0, 10.0, 11.0: for each, the eligible row with the nearest stored
  L∇B (ties: lowest row index), without reuse. If the nearest is more than 0.3 away, the target is dropped and reported.
- Plus N33's five plasmas and results (rows 60653, 2931, 46244, 23761, selected401) as recorded.

Intake and fit: identical to N33 (N32/make_input.py orientation-matched input with the selected401 template; make_wout.py;
make_target_spec.py with the N33 neutral circular seed, r = 0.4 m; fit_coils.py --seconds 1800 --check-seconds 900,
current margins, order 5, default objective, no interior term). Code: current upstream main at launch (recorded).
Control: refit selected401 with the same recipe at that commit. If its worse-shift boundary mean differs from N33's
0.00161 by more than 5%, the code is not equivalent: the five N33 plasmas are then refit too, and only same-commit
results enter the primary test.

Primary outcome: Spearman rho between stored L∇B (#76 value for selected401) and the worse-shift fine boundary mean
(acceptance_v2 'mean'). "Supports" rho <= -0.45 (one-sided 5% critical value, n = 15); "contradicts" rho >= 0;
otherwise inconclusive. A fit with no eligible candidate ranks worst (ties shared) and is listed.
Usability (reported, not a pass/fail): |rho| >= 0.7.
Secondary (descriptive only): Spearman rho of the boundary mean against max elongation, log10 QI, edge mirror ratio,
flux compression, vacuum well, |iota|/nfp; boundary max; interior RMS; geometry status; start RMS.
Errors on different targets are not acceptance-comparable; this is a difficulty-ranking test, and the fitter's
settings were developed on selected401. Wout/spec/fit failures are kept and reported, never replaced.
Budget: <= 12 h total, one thread, serial, <= 3 GiB output, 3 GiB/2 GiB disk reserve. No overlap with a Codex
native window (checked in its notes before each plasma).
