# C18 seeded controls: local launcher path freeze

Owner: existing autonomous Codex #112 role. State: READY only with a fresh current
owned claim and live resource gates. No model call has started. Public source:
a82a8def8c0051c2491cac38c577ad7813ab2c7c, scorer unchanged32fe8ecd198a8615549b1086bca37682290f4e57.

This snapshot supersedes only the executable path binding of pre-run archive
4df7fde2c2c2a1641cb6f4b6957c50fa25f67b4e (tag evidence-seeded-native-protocol-v2-2026-10-26).
Its nine input/label files, three support/test files, dataset card, MIT attribution,
original bytes and packaging correction remain at that immutable public identity.
No repeated model work, input, setting, comparator, tolerance or budget change.

PR137 review requested that workspace-specific coordination stay outside public
scripts/core CI. The launcher, manifest and tests now live under local ignored
results/c18-seeded-local/. Only import-path resolution changes: find the public
workflow via the frozen comparison protocol's repository, rather than beside the
relocated launcher. Original launcher/manifest/tests remain retained separately.
These are local workspace adapters, not a contributor interface or agent-granted
authority. User continuation authorizes the task; CAL-REQ-008 provides resource
coordination only. Other contributors can supply the workflow's check_ready hook.

New manifest SHA256:985505b9dc0c228d3722e87304222d17116f3bd58c77c0bf01fe0db7b4593702.
Copy these three files into worktrees/codex-autonomous/results/c18-seeded-local/;
use the v2snapshot layout for inputs/support and its scorer/runtime recipe.
Runtime binaries remain external with hashes; no environment changes here.
Default readiness command, from the owned source checkout:
`python3 results/c18-seeded-local/launch_seeded_constellaration.py --manifest results/c18-seeded-local/manifest.json --manifest-sha256 985505b9dc0c228d3722e87304222d17116f3bd58c77c0bf01fe0db7b4593702 --alignment-root <ROOT>`.
Add --execute only after a fresh manifest-specific owned checkpoint claim and
revalidation of the explicit CAL-REQ-008 seeded-only window26Oct06Z–28Oct06Z,
controller-held lock, <=60second inventory/no STOP. Empty inventory before launch;
only the owned native child may appear during execution. No peer process control.

Question: do all36 signed metrics comparisons agree for original rows146128,
141151,116646 at dataset8da71572? Cheapest decisive test: at most3serial default
high-fidelity calls, once per row, unchanged order. Comparison protocol SHA256
df71882af62631557cc4bad55472e7a0a1f0bdb665a7f9c51fb1c602bea7303b is unchanged.
Use abs(computed-stored)<=1e-8+1e-6*abs(stored), no fallback or replacement.
Mismatch continues; execution/settings/report/resource failure stops and is retained.
Limits1800global/1740child seconds, dual UTC/monotonic deadlines including late
completion/window end, one thread,100MiB output,3/2GiB reserves. No native startup
or agreement claim. Unknown historical producer limits attribution; mismatch is
not scorer fault or physical infeasibility. No other native lane or past-run retry.

Eight relocated launcher tests and five unchanged supervisor controls pass; the
549 bound files were reverified without model imports. Native integration remains
untested. A new dispatch must reserve its full native budget plus checkpoint time.
