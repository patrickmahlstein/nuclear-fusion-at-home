# N40 preregistration: replicate pair (run-to-run noise) for the N38/N39 objective result

N38/N39 single runs: local control 0.7978 (pass); p=1.5 0.7421 (pass); p=1.25 0.7302 (geometry unresolved) ->
certified_selection point 0.7323 (pass). Wall-clock budgets make reruns differ (evaluation counts vary).
N40 reruns local and mean-abs p=1.25 as a 2-parallel pair, identical to N38/N39 conditions and code (896abdf), with
certified_selection applied to any arm whose final geometry is unresolved (same rule for both arms).
Outcome: replicated effect if (p=1.25 worst, certified if needed) <= 0.95 * (local worst) again. Report both runs'
values; pooled means over N38/N39 + N40 descriptive only.
