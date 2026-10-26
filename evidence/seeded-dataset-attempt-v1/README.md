# Seeded dataset attempt: incomplete after geometry failure

One frozen task was executed once on 26 October 2026. Row 146128 completed the
forward model, but the unchanged geometry gate rejected its VMEC boundary.
Rows 141151 and 116646 were not run. The workflow and launch results are incomplete;
all_agree is false. No retry, replacement, tolerance or settings change occurred.

Producer/workflow source: clean 381e3d06ab864e1867c146ab87f952758f349b5e.
Scorer: clean 32fe8ecd198a8615549b1086bca37682290f4e57, file SHA256
1b394999a89891c84329e406ed8a80a3849c56151bb922ec291a86d73cf749d6.
Manifest SHA256 985505b9dc0c228d3722e87304222d17116f3bd58c77c0bf01fe0db7b4593702.
Comparison SHA256 df71882af62631557cc4bad55472e7a0a1f0bdb665a7f9c51fb1c602bea7303b.
Public pre-run freezes: issue112 comments 6410320103 and 6410424888.
Inputs/support: fork commit 4df7fde2c2c2a1641cb6f4b6957c50fa25f67b4e,
annotated evidence-seeded-native-protocol-v2-2026-10-26.
Local adapter source: fork commit 984ef766b3656c49ce9251b9bf731e3954a0ea2f,
annotated evidence-seeded-local-launcher-v1-2026-10-26.

Dataset: Proxima Fusion ConStellaration, pinned revision
8da71572eb63ce93e77ce89bec0d7c30b7eba89e; pinned card declares MIT.
Original selection, all three inputs and all twelve signed labels remain frozen.
Returned scalars for row146128 all fall within the arithmetic tolerance, as an
independent postflight diagnostic only. The invalid report cannot qualify a row.
Geometry residual vmec_boundary_vs_input is 0.3845235118440413 input units,
against 9.98755402197538e-11; coefficient bound 0.41309806980822056.
Surface/input residual is 1.1102230246251565e-15; its coefficient bound is zero.
VMEC ier_flag=0, ns99, mpol10, ntor10. No Wout was saved because the scorer checks
geometry before its optional save. Cause remains unresolved. These observations
do not establish scorer fault, historical producer identity, or physical infeasibility.

Forward model: 258.5169301970018 seconds. Native child: 316.7473419149901 monotonic /
316.74576592445374 UTC seconds, exit1, no deadline/resource stop, terminal
2026-10-26T07:41:02.759610+00:00. Whole launcher:321.0737577539985 monotonic /
321.0725476741791 UTC seconds. One thread; retained run payload137860 bytes at
child completion, below100MiB. Free disk after model55931965440 bytes.
CAL-REQ-008 was current; controller lock and fresh empty prelaunch inventory were
recorded. Only owned child35231 appeared while running; later inventory was empty.
All549bound files were unchanged after execution. Effective VMEC settings retained.

Original reproduction command (not permission to rerun):

```sh
python3 results/c18-seeded-local/launch_seeded_constellaration.py \
  --manifest results/c18-seeded-local/manifest.json \
  --manifest-sha256 985505b9dc0c228d3722e87304222d17116f3bd58c77c0bf01fe0db7b4593702 \
  --alignment-root <alignment-root> --execute
```

Runtime binaries remain external and hash-identified, not archived here. Original
raw files, cache and temporary outputs remain local and untouched. Archive excludes
cache/tmp only. Reports/tracebacks preserve inspected absolute local path strings
for byte identity; no credentials or private input data were found. This is a same-
machine numerical attempt, not external scientific review or physical acceptance.

Metadata correction: the v2 tag corrects the public freeze comment identifier
from6410359347 to6410320103. The original v1 tag remains unchanged. All run
payloads, settings, metrics, protocol, manifest and verdict bytes are unchanged.
