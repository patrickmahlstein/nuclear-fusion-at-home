# N41 preregistration: interior weight with the matched objective

With --flux-objective mean-abs --flux-power 1.25 (N39/N40: certified 0.732 twice, mean 0.73, max 0.72, interior 0.20),
the interior term has slack. Arms (2 parallel, same conditions/code 40258cb as N40): interior weight 0.02 and 0.01;
everything else identical (order 8, halved margins, 1800+900 s, N18 spec/seed/regen Wout).
Certified selection applied to any geometry-unresolved final point (same rule).
Outcome: worst v2 ratio vs 0.732 (w 0.05). "Helps" if <= 0.95*0.732 = 0.695; "comparable" within 5%; report all.
If interior fails v2 (> 0.01) the arm fails.
