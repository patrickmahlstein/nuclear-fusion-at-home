# N30 preregistration (#48): selected401 fit, same qualification (N28) and matched diagnostic (N29)

Inputs: archive 05a45110 selected401/fit/selected-snapshot.json (c2ea45c1..., matches manifest), frozen current;
Wout = REGENERATED selected401 3d5df9a4... (vmecpp 0.8.0), a substitute for the original 8cd6bebf... (maintainer-local).
Earlier N14: this regen reproduces the archived selected401 ideal narrow score to 1.0e-7 relative.
Scripts unchanged: N28 matched.py then N29 matched_bounce.py (same thresholds, domain, resolution).
Control: coil target-launch narrow score must reproduce archived 4.038923098070370e-5 (C7) to <= 1e-6 relative;
if not, matched results are reported but labelled "substitute Wout not qualified".
Reported: qualification table as N28; narrow scores ideal / target-launch / matched; difference between fits
under target launches (#35: -5.07%) and under matched launches. Descriptive, not a transfer claim (substitute Wout,
one seed per fit). Budget <= 1.5 h.
