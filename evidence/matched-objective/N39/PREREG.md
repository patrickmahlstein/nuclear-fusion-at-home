# N39 preregistration: Lp mean objective, p between the mean (p=1) and RMS (p=2)

N38 (paired, same recipe/seed/target): local L2 control worst v2 0.7978 (mean 0.001436, max 0.0081, geometry pass);
mean-abs (p=1) mean 0.001305 (-9.1%) but max 0.0107 (ratio 0.823, now binding) and continuous geometry unresolved
(coil lower bound 0.0598 vs 0.06; sampled 0.0648). Hypothesis: an intermediate p balances mean and max ratios.
Arms (2 in parallel, as N38): identical recipe (--order 8 --margins halved --interior-weight 0.05 --seconds 1800
--check-seconds 900), same N18 spec/seed/regen Wout, --flux-objective mean-abs --flux-power 1.25 and 1.5.
Code: N38 branch commit after ace5eb4 (flux power added; default path byte-identical, 427 tests).
Primary: worst v2 ratio with continuous geometry; compared with N38 control 0.7978 (same conditions).
"Helps" if best passing arm <= 0.95*0.7978 = 0.758; report all; geometry 'unresolved' arms reported as not passing,
then certified_selection.py (unchanged rule) applied to them as a disclosed secondary.
