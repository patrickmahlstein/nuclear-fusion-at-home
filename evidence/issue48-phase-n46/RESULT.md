# N46 result (#48)
Preregistered verdict: UNRESOLVED. Control reproduced (N28 metric at 60 transits 1.697 mm). N28 metric at 240 transits:
s=0.5 0.747 mm (pass), s=0.75 0.083 mm. Metric B as preregistered is invalid: iota per turn ~0.55 > 1/2, so unwrapping
the per-crossing angle aliases (rotation spread 0.019 at s=0.5; B fails the s=0.75 control, 1.23 mm).
Post-hoc (labelled, after the result; posthoc.py/posthoc2.py, saved crossings only): rotation by minimum-perimeter ordering.
s=0.75: rotation 0.47719 for all four phases, B 0.049 mm (control now passes). s=0.5: rotation 0.45425 per turn, 3.0e-4 from
5/11 (|iota| ~ 6/11); B 0.38-2.83 mm, asymmetric between phases. Target iota = -6/11 at s = 0.495 (regen Wout).
Reading: the s=0.5 cell sits on the iota = 6/11 rational surface (m=11, n=6=3*nfp, symmetry-allowed). Its phase spread is
most plausibly resonant (thin island chain or resonant surface below N34's visual resolution), not only construction.
Not proven: no island width measured. Recommendation for #40: do not use s=0.5 as a matched cell; pick cells away from
low-order rationals, or qualify them with a resonance-aware method.
