"""Replay the preregistered #113 calibration from verified projected Parquet ranges."""
import hashlib
import io
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PREFIX = 'metrics.'
METRICS = {
    'vacuum_well': ('vacuum_well', 0, 'lower'),
    'flux_compression': ('flux_compression_in_regions_of_bad_curvature', 0.9, 'upper'),
    'qi': ('qi', 1e-4, 'upper'),
    'edge_transform': ('edge_rotational_transform_over_n_field_periods', 0.25, 'abs_lower'),
    'mirror_ratio': ('edge_magnetic_mirror_ratio', 0.25, 'upper'),
}
OBJECTIVES = ['minimum_normalized_magnetic_gradient_scale_length', 'max_elongation']


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def passes(row, key):
    column, bound, direction = METRICS[key]
    value = row.get(PREFIX + column)
    if not finite(value) or (key == 'qi' and value < 0):
        return None
    if direction == 'abs_lower':
        return abs(value) >= bound
    return value >= bound if direction == 'lower' else value <= bound


def distribution(values):
    data = sorted(v for v in values if finite(v))
    result = {'valid': len(data), 'missing': len(values) - len(data)}
    def quantile(p):
        x = (len(data) - 1) * p
        lo, hi = math.floor(x), math.ceil(x)
        return data[lo] + (data[hi] - data[lo]) * (x - lo)
    result['quantiles'] = ({str(p): quantile(p) for p in [0, .05, .25, .5, .75, .95, 1]}
                           if data else None)
    return result


def summarize(rows, flags):
    total = len(rows)
    selected = [r for r in rows if finite(r.get('boundary.n_field_periods'))
                and r['boundary.n_field_periods'] == 2
                and finite(r.get(PREFIX + 'aspect_ratio'))
                and 9 <= r[PREFIX + 'aspect_ratio'] <= 11]
    def subset(data):
        size = len(data)
        criteria = {}
        for key in METRICS:
            states = [passes(r, key) for r in data]
            n = sum(v is True for v in states)
            valid = sum(v is not None for v in states)
            criteria[key] = {'pass': n, 'valid': valid, 'missing_invalid': size-valid,
                             'fraction_all': n/size if size else None,
                             'fraction_valid': n/valid if valid else None,
                             'rare': n/size < .01 if size else None, 'zero': n == 0}
        complete = [r for r in data if all(passes(r, k) is not None for k in METRICS)]
        joint = [r for r in complete if all(passes(r, k) for k in METRICS)
                 and all(r.get(f) is False for f in flags)]
        raw_joint = sum(all(passes(r, k) for k in METRICS) for r in complete)
        return {'rows': size, 'criteria': criteria, 'complete_metric_rows': len(complete),
                'joint': len(joint), 'metric_only_joint': raw_joint,
                'joint_fraction_all': len(joint)/size if size else None,
                'joint_fraction_complete': len(joint)/len(complete) if complete else None,
                'joint_rare': len(joint)/size < .01 if size else None,
                'joint_zero': not joint,
                'error_flags': {f: {'true': sum(r.get(f) is True for r in data),
                                    'unknown': sum(not isinstance(r.get(f), bool) for r in data)}
                                for f in flags},
                'negative_signed_transform': sum(finite(r.get(PREFIX+METRICS['edge_transform'][0]))
                                                  and r[PREFIX+METRICS['edge_transform'][0]] < 0
                                                  for r in data),
                'zero_qi': sum(finite(r.get(PREFIX+'qi')) and r[PREFIX+'qi'] == 0 for r in data),
                'distributions': {scope: {m: distribution([r.get(PREFIX+m) for r in population])
                                         for m in OBJECTIVES}
                                  for scope, population in [('selected', data), ('joint', joint)]},
                'joint_ids': [r.get('plasma_config_id') for r in joint]}
    groups = defaultdict(list)
    for row in selected:
        groups[row.get('plasma_config_id')].append(row)
    fields = [PREFIX+c for c, _, _ in METRICS.values()] + [PREFIX+c for c in OBJECTIVES] + flags
    def signature(row):
        return tuple(repr(row.get(f)) for f in fields)
    consistent = [items[0] for key, items in groups.items() if key is not None
                  and len({signature(r) for r in items}) == 1]
    return {'total_rows': total,
            'missing_selection_fields': sum(r.get('boundary.n_field_periods') is None
                                            or r.get(PREFIX+'aspect_ratio') is None for r in rows),
            'malformed_nonnull_selection_fields': sum(
                any(r.get(k) is not None and not finite(r.get(k))
                    for k in ['boundary.n_field_periods', PREFIX+'aspect_ratio']) for r in rows),
            'invalid_selection_fields': sum(not finite(r.get('boundary.n_field_periods'))
                                           or not finite(r.get(PREFIX+'aspect_ratio')) for r in rows),
            'selected': subset(selected), 'distinct_nonnull_ids': sum(k is not None for k in groups),
            'missing_ids': sum(r.get('plasma_config_id') is None for r in selected),
            'duplicate_ids': sum(k is not None and len(v)>1 for k,v in groups.items()),
            'conflicting_ids': sum(k is not None and len({signature(r) for r in v})>1
                                   for k,v in groups.items()),
            'consistent_unique_sensitivity': subset(consistent)}


class VerifiedRanges(io.RawIOBase):
    def __init__(self, entry, manifest):
        self.entry, self.pos, self.parts = entry, 0, []
        stem = Path(entry['path']).stem
        for key, digest in manifest.items():
            if not key.startswith(stem+'-'):
                continue
            start, end = map(int, key[len(stem)+1:-len('.range')].split('-'))
            data = (ROOT/key).read_bytes()
            if len(data) != end-start+1 or hashlib.sha256(data).hexdigest() != digest:
                raise ValueError('range integrity failure: '+key)
            self.parts.append((start, end, data))
    def readable(self):
        return True
    def seekable(self):
        return True
    def tell(self):
        return self.pos
    def seek(self, offset, whence=0):
        self.pos = offset if whence == 0 else self.pos+offset if whence == 1 else self.entry['size']+offset
        return self.pos
    def read(self, n=-1):
        if n < 0:
            n = self.entry['size']-self.pos
        n = min(n, self.entry['size']-self.pos)
        if n == 0:
            return b''
        for start, end, data in self.parts:
            if start <= self.pos and self.pos+n-1 <= end:
                result = data[self.pos-start:self.pos-start+n]
                self.pos += n
                return result
        raise ValueError(f'unavailable range {self.pos}:{self.pos+n}')
    def readinto(self, buffer):
        data = self.read(len(buffer))
        buffer[:len(data)] = data
        return len(data)


def self_test():
    # Exact-bound controls, missingness, negative QI, signed transform and error exclusion.
    row = {'boundary.n_field_periods': 2, 'metrics.aspect_ratio': 10,
           'plasma_config_id': 'control', 'misc.has_test_error': False}
    for key, (column, bound, _) in METRICS.items():
        row[PREFIX+column] = bound
    row[PREFIX+METRICS['edge_transform'][0]] = -.25
    data = summarize([row], ['misc.has_test_error'])['selected']
    assert data['joint'] == 1 and data['negative_signed_transform'] == 1
    assert summarize([{**row, 'misc.has_test_error': True}], ['misc.has_test_error'])['selected']['joint'] == 0
    assert summarize([{**row, 'metrics.qi': None}], ['misc.has_test_error'])['selected']['complete_metric_rows'] == 0
    assert passes({**row, 'metrics.qi': -1}, 'qi') is None
    assert passes({**row, 'metrics.qi': 0}, 'qi') is True
    assert passes({**row, 'metrics.qi': 1.00000001e-4}, 'qi') is False
    assert distribution([0, 10, None])['quantiles']['0.25'] == 2.5
    assert summarize([row, {**row, 'metrics.qi': 0}], ['misc.has_test_error'])['conflicting_ids'] == 1
    print('analytic controls passed')


def main():
    if '--self-test' in sys.argv:
        self_test()
        return
    import pyarrow
    import pyarrow.parquet as pq
    plan = json.loads((ROOT/'range-plan.json').read_text())
    manifest = json.loads((ROOT/'ranges.json').read_text())
    rows = []
    for item in plan:
        file = pq.ParquetFile(VerifiedRanges(item['entry'], manifest), pre_buffer=False)
        columns = item['columns']
        if not set(columns).issubset(file.schema_arrow.names):
            raise ValueError('required columns missing')
        rows.extend(file.read(columns=columns, use_threads=False).to_pylist())
    flags = [c for c in plan[0]['columns'] if c.startswith('misc.has_')]
    report = summarize(rows, flags)
    report['identities'] = {'dataset_revision': '8da71572eb63ce93e77ce89bec0d7c30b7eba89e',
                            'python': sys.version, 'pyarrow': pyarrow.__version__,
                            'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                            'range_manifest_sha256': hashlib.sha256((ROOT/'ranges.json').read_bytes()).hexdigest(),
                            'range_bytes': sum((ROOT/k).stat().st_size for k in manifest),
                            'input_files': [p['entry'] for p in plan]}
    Path(sys.argv[1]).write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in report['selected'].items() if k in ['rows','joint','criteria']}, indent=2))


if __name__ == '__main__':
    main()
