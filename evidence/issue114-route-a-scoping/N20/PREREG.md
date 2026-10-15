# N20 preregistration (exploratory, #114 route A) — 2026-10-15 ~06:45Z

Question: can selected401 reach FC <= 0.85 while keeping W >= 0.005, aspect fixed and iota/nfp >= start,
on the native mirror (ns99, as N19), using low-order boundary modes (m<=3, |n|<=3)?
Start: N19 least-norm step dx at scale 1 (W +0.0027, FC 1.348).
Step 1 (secant.py): one-sided h=5e-3 on every nonzero low-order mode around start; h=2.5e-3 check on
rbc(1,0), rbc(2,0), zbs(1,1), zbs(2,-2); FC "large-step smooth" if the two slopes agree within 25%.
Step 2 (repair.py, modes restricted to step-1 set): trust-region Gauss-Newton with Broyden updates,
scaled residual on goals (W>=0.005, FC<=0.85, A=A_start, iota/nfp>=iota_start), initial radius 0.01,
accept on merit decrease, <=25 iterations or 30 min. Edge mirror ratio recorded, not constrained.
Outcome: report best accepted state; "repair found (mirror)" only if all four goals met and ier=0.
Then confirm best state at ns=401 (one solve) with the same mirror. No QI/elongation claims: hand the
boundary to the #112 scorer. Budget: 1 h step 1 + 30 min step 2 + 10 min confirm, one thread.
