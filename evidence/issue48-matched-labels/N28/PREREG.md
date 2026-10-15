# N28 preregistration (#48): surface-matched launches on the #35 reference401 fit

Inputs: archive evidence-issue25-matched-v1 commit 05a45110, reference401/fit/selected-snapshot.json (ec1f8ce7...),
frozen current 1e5*scale; regenerated reference401 Wout 0f2b626c (vmecpp 0.8.0). SIMSOPT 1.11.1, one thread.
Label construction: N9 run 2 (periodic spline through phi=0 crossings ordered about realized axis, Phi = loop A.dl,
s_real = Phi/Phi_edge, Phi_edge on exact target boundary section). Assumptions: crossings star-shaped about the
axis; spline is a construction, not proof of a magnetic surface.
Matching: 20 cases (s in 0.1/0.25/0.5/0.75/0.9 x theta 0, pi/2, pi, 3pi/2). Launch at target position of
continuous label sigma (linear interpolation between full-grid surfaces). Secant on sigma, start sigma=s,
<=5 batched traces, 60 transits, tol 1e-10. Matched if |s_real - s| <= 1e-3; unmatched kept as failures.
Phase consistency: per s, max distance of any matched line's crossings to another phase's spline. Pass if
<= 1 mm (assignable to one curve); else report "phases not one surface".
Sensitivity: matched sigma re-traced with 120 transits and with tol 1e-11; pass if |Delta s_real| <= 1e-3.
Budget <= 1 h. Next step (action diagnostic on matched labels) only after this, with its own preregistration.
