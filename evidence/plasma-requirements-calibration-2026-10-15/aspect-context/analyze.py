"""Exploratory stored-label aspect/NFP context, without admission or seed selection."""
import hashlib
import importlib.util
import json
import math
import shutil
import sys
import time
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

CACHE = Path(sys.argv[1]).resolve()
OUTPUT = Path(sys.argv[2])
START = time.monotonic()
assert shutil.disk_usage(OUTPUT.parent).free >= 3 * 1024**3
spec = importlib.util.spec_from_file_location('verified_reader', CACHE / 'calibrate.py')
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)
assert hashlib.sha256((CACHE / 'calibrate.py').read_bytes()).hexdigest() == (
    '25e96145b76b860961b8a6e0a2e4ad6e047d498a08321a2da741c5a23a30316f')
manifest_bytes = (CACHE / 'ranges.json').read_bytes()
assert hashlib.sha256(manifest_bytes).hexdigest() == (
    '15c98aade58e3e0d34b55a1d36b0f7733a0c4fbef5b81293858688bf97cbc403')
manifest = json.loads(manifest_bytes)
plan = json.loads((CACHE / 'range-plan.json').read_text(encoding='utf-8'))
pa.set_cpu_count(1)
pa.set_io_thread_count(1)

CHECKS = [
    ('vacuum_well', lambda x: x >= 0),
    ('flux_compression_in_regions_of_bad_curvature', lambda x: x <= 0.9),
    ('qi', lambda x: 0 <= x <= 1e-4),
    ('edge_rotational_transform_over_n_field_periods', lambda x: abs(x) >= 0.25),
    ('edge_magnetic_mirror_ratio', lambda x: x <= 0.25),
]
EDGES = [0, 4, 6, 8, 10, 12, 16, None]
LABELS = ['[0,4)', '[4,6)', '[6,8)', '[8,10)', '[10,12)', '[12,16)', '[16,infinity)']
FLAGS = [name for name in plan[0]['columns'] if name.startswith('misc.has_')]
FORWARD = 'misc.has_neurips_2025_forward_model_error'


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def empty():
    return dict(rows=0, complete_metrics=0, metric_joint=0,
                metric_joint_forward_false=0, original_strict_flag_joint=0,
                all_five_historical_flags_known=0,
                forward_error_true=0, forward_error_false=0, forward_error_unknown=0,
                marginals={name: dict(valid=0, passes=0) for name, _ in CHECKS})


def add(counter, row, states):
    counter['rows'] += 1
    complete = all(state is not None for state in states)
    joint = all(state is True for state in states)
    counter['complete_metrics'] += complete
    counter['metric_joint'] += joint
    counter['all_five_historical_flags_known'] += all(type(row.get(f)) is bool for f in FLAGS)
    forward = row.get(FORWARD)
    counter['forward_error_true' if forward is True else 'forward_error_false'
            if forward is False else 'forward_error_unknown'] += 1
    counter['metric_joint_forward_false'] += joint and forward is False
    counter['original_strict_flag_joint'] += joint and all(row.get(f) is False for f in FLAGS)
    for (name, _), state in zip(CHECKS, states, strict=True):
        counter['marginals'][name]['valid'] += state is not None
        counter['marginals'][name]['passes'] += state is True


def finish(counter):
    n, valid = counter['rows'], counter['complete_metrics']
    counter['metric_joint_fraction_population'] = counter['metric_joint'] / n if n else None
    counter['metric_joint_fraction_complete'] = counter['metric_joint'] / valid if valid else None
    for value in counter['marginals'].values():
        value['fraction_population'] = value['passes'] / n if n else None
        value['fraction_valid'] = value['passes'] / value['valid'] if value['valid'] else None
    return counter


cohorts = {key: dict(all_rows=0, excluded_aspect_missing=0, excluded_aspect_invalid=0,
                    positive_aspect_total=empty(), bins={label: empty() for label in LABELS})
           for key in [f'nfp_{i}' for i in range(1, 6)] + ['nfp_1_to_5']}
primary = empty()
global_rows = 0
global_qi_valid = 0
global_qi_pass = 0
nfp_missing = 0
nfp_invalid = 0
other_nfp = {}
for item in plan:
    parquet = pq.ParquetFile(reader.VerifiedRanges(item['entry'], manifest), pre_buffer=False)
    for group in range(parquet.num_row_groups):
        assert time.monotonic() - START < 180
        assert shutil.disk_usage(OUTPUT.parent).free >= 2 * 1024**3
        rows = parquet.read_row_group(group, columns=item['columns'], use_threads=False).to_pylist()
        for row in rows:
            global_rows += 1
            qi = row.get('metrics.qi')
            if finite(qi) and qi >= 0:
                global_qi_valid += 1
                global_qi_pass += qi <= 1e-4
            nfp, aspect = row.get('boundary.n_field_periods'), row.get('metrics.aspect_ratio')
            if nfp is None:
                nfp_missing += 1
                continue
            if not finite(nfp) or nfp != int(nfp) or nfp <= 0:
                nfp_invalid += 1
                continue
            if nfp not in range(1, 6):
                other_nfp[str(nfp)] = other_nfp.get(str(nfp), 0) + 1
                continue
            keys = [f'nfp_{int(nfp)}', 'nfp_1_to_5']
            for key in keys:
                cohorts[key]['all_rows'] += 1
            if aspect is None:
                for key in keys:
                    cohorts[key]['excluded_aspect_missing'] += 1
                continue
            if not finite(aspect) or aspect <= 0:
                for key in keys:
                    cohorts[key]['excluded_aspect_invalid'] += 1
                continue
            states = []
            for name, test in CHECKS:
                value = row.get('metrics.' + name)
                valid = finite(value) and (name != 'qi' or value >= 0)
                states.append(test(value) if valid else None)
            index = next(i for i, upper in enumerate(EDGES[1:]) if upper is None or aspect < upper)
            for key in keys:
                add(cohorts[key]['positive_aspect_total'], row, states)
                add(cohorts[key]['bins'][LABELS[index]], row, states)
            if nfp == 2 and 9 <= aspect <= 11:
                add(primary, row, states)

original = json.loads((CACHE / 'calibration.json').read_text(encoding='utf-8'))
assert global_rows == original['total_rows']
assert primary['rows'] == original['selected']['rows']
assert primary['metric_joint'] == original['selected']['metric_only_joint']
for short, (name, _) in zip(['vacuum_well', 'flux_compression', 'qi', 'edge_transform',
                           'mirror_ratio'], CHECKS, strict=True):
    assert primary['marginals'][name]['passes'] == original['selected']['criteria'][short]['pass']
assert (global_qi_valid, global_qi_pass) == (158685, 9)
for key, cohort in cohorts.items():
    total = cohort['positive_aspect_total']
    assert cohort['all_rows'] == (total['rows'] + cohort['excluded_aspect_missing']
                                  + cohort['excluded_aspect_invalid'])
    for field in ['rows', 'complete_metrics', 'metric_joint', 'metric_joint_forward_false',
                  'original_strict_flag_joint']:
        assert total[field] == sum(value[field] for value in cohort['bins'].values())
    for name, _ in CHECKS:
        for field in ['valid', 'passes']:
            assert total['marginals'][name][field] == sum(
                value['marginals'][name][field] for value in cohort['bins'].values())
    finish(total)
    for value in cohort['bins'].values():
        finish(value)
for field in ['rows', 'complete_metrics', 'metric_joint']:
    assert cohorts['nfp_1_to_5']['positive_aspect_total'][field] == sum(
        cohorts[f'nfp_{i}']['positive_aspect_total'][field] for i in range(1, 6))
report = dict(
    scope='Exploratory stored-label context; no admission, threshold change or seed selection.',
    dataset_revision='8da71572eb63ce93e77ce89bec0d7c30b7eba89e',
    primary_evidence_commit='0efdc425c56d55cbc5d09090888c9748650d77ce',
    protocol_comment='https://github.com/DrWorkhard/nuclear-fusion-at-home/issues/113#issuecomment-6184923865',
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    range_manifest_sha256=hashlib.sha256(manifest_bytes).hexdigest(),
    global_rows=global_rows, global_valid_nonnegative_qi=global_qi_valid,
    global_qi_passes=global_qi_pass, missing_nfp=nfp_missing, invalid_nfp=nfp_invalid,
    nfp_outside_1_to_5=other_nfp, aspect_edges=EDGES,
    primary_closed_slice=finish(primary), cohorts=cohorts,
    checks=['Primary counts and all marginals reproduce.', 'Global valid QI/pass counts reproduce.',
            'Bin counters sum to separately accumulated cohort counters.',
            'Pooled NFP counts sum to individual cohorts.'],
    limitations=['Stored labels await issue112 producer/fidelity controls.',
                 'Unknown/inapplicable historical flags are not demonstrated solver failures.',
                 'No independent-family feasibility probabilities or native confirmation.'])
OUTPUT.write_text(json.dumps(report, indent=2, allow_nan=False) + '\n', encoding='utf-8')
print(json.dumps({key: {'rows': value['positive_aspect_total']['rows'],
                        'joint': value['positive_aspect_total']['metric_joint']}
                  for key, value in cohorts.items()}, indent=2))
