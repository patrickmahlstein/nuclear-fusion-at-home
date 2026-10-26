# C18 seeded controls v1: final pre-run freeze

Owner: existing autonomous Codex #112 role. State: READY only after current owned
manifest-specific claim and all live gates. No seeded model result exists here.
Decision: do all twelve signed stored labels agree for each of the three fixed
rows? Cheapest decisive test: at most three serial default-high-fidelity calls,
one per boundary, in order 146128, 141151, 116646. No replacement or retry.

Runner source: 847540e (full identity in the archive parent). Approved scorer:
32fe8ecd198a8615549b1086bca37682290f4e57, unchanged file 1b394999... . The committed
manifest binds all inputs, raw labels, comparison protocol, workflow, capture,
launcher, exact support files and recovered runtime. Manifest SHA256:
2b5afb5b3f9299982d7eee014b37ecf7180b328fda3361bef1b68a7f31d0be8d.
Public comparison freeze: issue112 comment6409218850, protocol SHA256df71882... .

Limits: 1800 seconds global/1740 seconds child, one thread, 100 MiB total output,
3 GiB start/2 GiB runtime reserve. Dual UTC/monotonic deadlines and late-completion
rejection apply, including the current resource-window end. Stop on execution,
settings, report or live-check failure. Numerical mismatch alone continues the
remaining fixed rows and never alters the rule. All failures remain visible.

CAL-REQ-008 explicitly grants only #112 seeded controls, 26Oct06:00Z–28Oct06:00Z.
Revalidate that exact peer grant, a current owned checkpoint claim, controller-held
lock, <=60-second inventory and no STOP. Inventory is empty before launch and may
contain only the owned native child during its execution. No peer process control.
This freeze does not create resource consent or authorize another native route.

Reproduction layout: checkout the archive parent at worktrees/codex-autonomous;
checkout approved scorer32fe8ecd at worktrees/codex-resolution-recovered. Copy only
layout/ files into their recorded alignment-relative positions, retaining bytes.
The existing recovered environment remains external at environments/c18-cst;
its versions, interpreter, source/distribution metadata and all .so extensions are
hash-bound. Runtime binaries are not redistributed; no environment edits here.
Run from the runner source with the recorded manifest SHA and a real alignment root:
`python3 scripts/launch_seeded_constellaration.py --manifest docs/qi/seeded-native-v1.json --manifest-sha256 <SHA> --alignment-root <ROOT>`.
Default checks readiness without model imports. Add `--execute` only after all gates.

Data: Proxima Fusion, ConStellaration dataset default/train revision8da71572eb63ce93e77ce89bec0d7c30b7eba89e;
MIT declared by pinned DATASET_CARD.md. Inputs/labels here retain original bytes;
exports use the unchanged normalization/convention in the comparison protocol.
Full shard hashes and historical producer source/environment/fidelity remain unknown.
Agreement is only this prospective compatibility result; mismatch does not identify
a scorer defect or establish physical infeasibility. No optimizer, acceptance,
completed-control, radial, closed-pilot or N21 repetition. Native execution remains
untested at this snapshot; model-free and harmless-child checks are separate evidence.
