# Registered-target replay for the partial plasma scorecard

These are unchanged report, reference, comparison and Wout bytes from the single
completed C18 N23 replay on 16 October 2026. `manifest.json` binds all payloads.
Both targets completed and their metrics/settings/benchmark projection match N23
exactly. This is a software regression control, not full scorer qualification.

Producer: clean `60d515001562c5da713be5ec5880629c2f92aa1a`.
Command (from that checkout, separate pinned environment):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  <pinned-python> scripts/constellaration_metrics.py --output <new-dir>
```

Exact interpreter/package versions and effective settings are in `report.json`.
The installed environment has since vanished from temporary storage. Recreating
its package versions does not establish identical binary bytes. No replay was
repeated to prepare this archive. Missing runtime and original local-only logs
remain explicit availability limits. Wouts and reports are retained unchanged.

Original public result and frozen comparison:
https://github.com/DrWorkhard/nuclear-fusion-at-home/issues/112#issuecomment-6209013504
https://github.com/DrWorkhard/nuclear-fusion-at-home/issues/112#issuecomment-6198513171

Seeded dataset validation, radial sensitivity and other historical-plasma scoring
remain incomplete. No physical acceptance follows from this snapshot.
