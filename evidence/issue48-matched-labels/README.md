# Evidence: #48 surface-matched launches (N28-N30)

Raw records for docs/optimization/ISSUE48_MATCHED_LABELS.md. N28: qualification on the #35 reference401 fit;
N29: narrow-domain bounce action from matched launches (reference401 fit); N30: both steps on the selected401 fit with
the regenerated selected401 Wout 3d5df9a4 (substitute for 8cd6bebf). Each folder: PREREG.md with SHA-256 written
before running, script, result JSON, log, result SHA-256. Inputs: archive commit 05a45110 snapshots (ec1f8ce7, c2ea45c1).
Run: python N28/matched.py SNAPSHOT WOUT OUT.json; python N29/matched_bounce.py SNAPSHOT WOUT OUT.json N28/matched.py
(repository root, one thread, native environment).
