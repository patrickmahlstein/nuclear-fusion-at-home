~01:25Z first launch: row 60653 make_wout rejected the Wout ("boundary differs from input rbc: 0.164"). Cause: dataset
boundaries wind poloidally opposite to our input convention; VMEC++ re-orients internally, so the Wout coefficients
differ from the input. Fix (converter only, before any fit ran): flip theta -> -theta when the phi=0 section's winding
differs from selected401's (all 4 rows flipped); verified on row 60653 with a coarse solve (boundary match 2e-18).
The flip is the same surface. Pipeline also now calls the converter with the native python (needs numpy). Restarted.
~02:50Z STOPPED after the first plasma. Row 60653: Wout/spec ok (iota_edge +0.638); fit ran 4,700 evaluations in 1800 s
but no eligible candidate (late trial: boundary RMS 0.021, max 0.15, coil curvature 10.37 > limit) -> "completed headroom
candidate ... required". Diagnosis: seed-handedness confound. Dataset plasmas have iota > 0 (mirror images of ours, iota < 0);
the length-headroom seed twists the wrong way. Remaining arms would measure the confound, not L∇B. Replaced by N33
(mirrored seed). Row 2931 was mid-Wout when stopped; no fit started for it.
