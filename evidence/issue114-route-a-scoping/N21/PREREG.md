# N21 preregistration (exploratory, #114 route A) — written after N20 result

Motivation: N20 reduced FC 1.348 -> ~1.08 but edge mirror rose 0.270 -> ~0.43 (> 0.25 bound).
Question: with edge mirror <= 0.24 added as a goal, what FC is reachable near selected401 (nfp=2)?
Same as N20 (start = N19 dx, secant Jacobian from N20 incl. mirror row, Broyden, trust region,
<=25 iterations / 30 min), residual adds max(mirror-0.24,0)/0.01. Report best accepted state:
FC, W, A, iota, mirror. No v1 claim; any finalist to #112 scorer.
