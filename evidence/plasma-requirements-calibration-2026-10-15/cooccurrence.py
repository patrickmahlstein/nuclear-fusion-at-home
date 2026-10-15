"""Exploratory exact-bound co-occurrence; no boundary selection or gate changes."""
import hashlib
import importlib.util
import itertools
import json
import math
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

started = time.monotonic()
cache = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2])
assert shutil.disk_usage(output.parent).free >= 3*1024**3
spec = importlib.util.spec_from_file_location('verified_data_reader', cache/'calibrate.py')
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)
assert hashlib.sha256((cache/'calibrate.py').read_bytes()).hexdigest() == (
    '25e96145b76b860961b8a6e0a2e4ad6e047d498a08321a2da741c5a23a30316f')
plan = json.loads((cache/'range-plan.json').read_text(encoding='utf-8'))
manifest = json.loads((cache/'ranges.json').read_text(encoding='utf-8'))
pa.set_cpu_count(1)
pa.set_io_thread_count(1)


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


checks = [
    ('vacuum_well', lambda value: value >= 0),
    ('flux_compression_in_regions_of_bad_curvature', lambda value: value <= .9),
    ('qi', lambda value: 0 <= value <= 1e-4),
    ('edge_rotational_transform_over_n_field_periods', lambda value: abs(value) >= .25),
    ('edge_magnetic_mirror_ratio', lambda value: value <= .25),
]
flags = [c for c in plan[0]['columns'] if c.startswith('misc.has_')]
masks = Counter()
selected = 0
invalid = 0
flag_complete = 0
flag_false = 0
# Independent direct subset accumulation cross-checks the histogram-derived result.
direct = Counter()
for item in plan:
    file = pq.ParquetFile(reader.VerifiedRanges(item['entry'], manifest), pre_buffer=False)
    for group in range(file.num_row_groups):
        assert time.monotonic()-started < 180
        assert shutil.disk_usage(output.parent).free >= 2*1024**3
        rows = file.read_row_group(group, columns=item['columns'], use_threads=False).to_pylist()
        for row in rows:
            nfp, aspect = row.get('boundary.n_field_periods'), row.get('metrics.aspect_ratio')
            if not (finite(nfp) and nfp == 2 and finite(aspect) and 9 <= aspect <= 11):
                continue
            selected += 1
            values = [row.get('metrics.'+name) for name, _ in checks]
            if not all(finite(value) for value in values) or values[2] < 0:
                invalid += 1
                continue
            states = [test(value) for value, (_, test) in zip(values, checks, strict=True)]
            mask = sum(1 << i for i, state in enumerate(states) if state)
            masks[mask] += 1
            flag_complete += all(type(row.get(f)) is bool for f in flags)
            flag_false += all(row.get(f) is False for f in flags)
            for required in range(32):
                direct[required] += all(states[i] for i in range(5) if required & (1 << i))
subsets = []
for required in range(32):
    count = sum(count for mask, count in masks.items() if mask & required == required)
    assert count == direct[required], ('histogram/direct mismatch', required)
    subsets.append({'mask': required, 'requires': [checks[i][0] for i in range(5)
                                                 if required & (1 << i)], 'count': count})
primary = json.loads((cache/'calibration.json').read_text(encoding='utf-8'))['selected']
assert selected == primary['rows'] and invalid == 0
for i, key in enumerate(['vacuum_well', 'flux_compression', 'qi', 'edge_transform', 'mirror_ratio']):
    assert direct[1 << i] == primary['criteria'][key]['pass']
assert direct[31] == primary['metric_only_joint']
result = {
    'scope': 'exploratory co-occurrence, exact original bounds; no subset is an admission rule',
    'dataset_revision': '8da71572eb63ce93e77ce89bec0d7c30b7eba89e',
    'range_manifest_sha256': hashlib.sha256((cache/'ranges.json').read_bytes()).hexdigest(),
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'selected': selected, 'invalid_metrics': invalid,
    'all_five_flags_known': flag_complete, 'all_five_flags_false': flag_false,
    'bit_order': [name for name, _ in checks],
    'exact_masks': [{'mask': i, 'pass': [checks[j][0] for j in range(5) if i & (1 << j)],
                     'count': masks[i]} for i in range(32)],
    'subset_intersections': subsets,
    'pairwise': [{'left': checks[i][0], 'right': checks[j][0], 'count': direct[(1 << i) | (1 << j)]}
                 for i, j in itertools.combinations(range(5), 2)],
    'checks': ['all 32 histogram/direct counts agree', 'primary five marginals and joint reproduced'],
    'limitations': ['Stored producer/fidelity not established; #112 controls pending.',
                    'Shared reader/PyArrow; not independent data or external peer review.',
                    'Exploratory diagnostics after primary zero joint-pass observation.'],
}
output.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n', encoding='utf-8')
print(json.dumps({'selected': selected, 'invalid': invalid,
                  'non_qi_four_bound_intersection': direct[27],
                  'pairs': result['pairwise']}, indent=2))
