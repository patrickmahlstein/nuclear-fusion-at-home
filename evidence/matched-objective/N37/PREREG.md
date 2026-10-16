# N37 preregistration: multistart from neutral circular seeds with the best 30-min recipe (leaderboard)

Question: does starting the best known 30-min recipe (#102 arm A: --order 8 --margins halved --interior-weight 0.05,
--seconds 1800 --check-seconds 900) from neutral circular seeds instead of the length-headroom chain give a better
acceptance-v2 worst ratio on selected401?
Target: selected401 via --target-spec on the regenerated Wout 3d5df9a4 (B2 agrees with registered to 1.5e-11;
interior to ~5e-11), so ratios are comparable to the leaderboard to that precision but the target identity differs.
Seeds (fixed now): make_circular_seed.py radius 0.38 / 0.40 / 0.45; all pass continuous start geometry.
Runs: 3 in parallel, one thread each, on an otherwise idle 8-core machine (no other native job).
Comparator: #102 arm A worst ratio 0.7779 (same recipe and budget, length-headroom seed).
Outcome rule: "better basin" if the best v2-passing arm (continuous geometry pass) has worst ratio <= 0.739 (5% bar
from #109); "comparable" if <= 0.778; else "worse". Report all three arms, failures kept.
Not acceptance-of-record (different target identity); a follow-up on the registered target is the maintainer's.
