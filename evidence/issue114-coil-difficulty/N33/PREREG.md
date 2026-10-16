# N33 preregistration (replaces N32 after its seed confound): does higher L∇B make coil fitting easier?

Same plasmas, intake and primary outcome as N32 (rows 60653 / 2931 / 46244 / 23761 with L∇B 3.00 / 4.50 / 6.99 / 7.41,
plus selected401 6.14; orientation-matched inputs; make_wout + make_target_spec). Change: a NEUTRAL seed for every
plasma, chosen before any N33 fit: 6 planar circular coils, radius 0.4 m, each centred on the plasma's phi-section
centre (m = 0 boundary terms) at phi_i = (i+0.5)(pi/nfp)/6. Startup control (done): passes continuous geometry on
selected401 and row 60653 (plasma clearance 0.145 / 0.117 m, coil spacing 0.14 m, length 2.52 m).
Reason (N32/DEVIATIONS.md): the length-headroom seed starts at boundary RMS 0.41 on dataset plasmas (mirrored too)
and its fit found no eligible candidate; it encodes selected401's shape, so it would measure seed fit, not L∇B.
Fit: fit_coils.py --seconds 1800 --check-seconds 900, current margins, order 5, no interior term (identical for all).
Primary: Spearman rho(L∇B, worse-shift fine boundary mean); "supports" rho <= -0.9, "contradicts" rho >= 0,
otherwise inconclusive. A plasma whose fit yields no eligible candidate is ranked worst (tie if several) and listed.
Secondary: boundary max, interior RMS, geometry, start RMS, max elongation as alternative proxy.
Errors on different targets are not acceptance-comparable. Budget <= 5 h, one thread.
