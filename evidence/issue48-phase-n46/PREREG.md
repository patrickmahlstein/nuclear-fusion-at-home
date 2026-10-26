# N46 preregistration (#48): is the selected401 fit's s = 0.5 phase failure a construction artifact?

N30 qualification: the four θ-phase lines matched to s_real = 0.5 lie up to 1.70 mm from each other's splines (limit 1 mm);
s = 0.1/0.25/0.75 pass (<= 0.08 mm). N34 Poincaré: nested, monotone labels, no island near s = 0.5. Hypothesis: the
N28 construction orders crossings by geometric angle about the axis and splines them; at the thin crescent's tips this
misorders/overshoots.
Decision: whether #40's matched-label comparison may use the s = 0.5 cell without a qualification failure.
Inputs: #35 selected401 fit snapshot c2ea45c1... at its frozen current; regenerated Wout 3d5df9a4...; N30's matched
launch labels sigma for s = 0.5 and 0.75 (control), all four phases. Direct Biot-Savart, SIMSOPT 1.11.1, one thread.
Method: trace each line 240 transits (tol 1e-11), phi = 0 crossings. Construction-free ordering: the k-th crossing of a
line on a flux surface sits at straight-field-line angle 2*pi*frac(k*iota); iota = rotation number from the unwrapped
geometric angle about the N28 axis over all crossings. Metric A: N28's metric (angle-ordered periodic spline) at
60 transits (must reproduce 1.70 mm within 0.1 mm: control). Metric B: max distance of each line's crossings to the
closed polyline of each other phase ordered by frac(k*iota) (point-to-segment). Also: per-phase rotation numbers.
Rule: "artifact" if B <= 1 mm at s = 0.5 and 0.75 and the four s = 0.5 rotation numbers agree to <= 1e-4;
"real" if B > 1 mm at s = 0.5 with B <= 1 mm at 0.75; otherwise "unresolved". Budget <= 1.5 h, one thread.
