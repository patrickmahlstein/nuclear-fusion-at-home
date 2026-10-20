# N43 preregistration: best matched-objective recipe at the 4-hour budget

Recipe (N41/N42 best, 30 min: 0.7165 / 0.7164): --order 8 --margins halved --interior-weight 0.02
--flux-objective mean-abs --flux-power 1.25, --seconds 14400 --check-seconds 1800 (4-hour cap of fit_coils),
same N18 spec/seed/regen Wout, code 896abdf, single process (no parallel job).
Comparator: best passing 4-hour leaderboard entries #109 W 0.7607 / S 0.7645 (default objective).
Certified selection applied if the final geometry is unresolved (same rule as #109 S).
Report: worst v2 ratio, components, geometry; "improves on #109" if <= 0.95*0.7607 = 0.723 and v2 passes.
Not leaderboard-of-record (regenerated Wout).
