"""Software controls: no model imports or scientific calculations."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
import json

import run_pair as pair

ROOT = Path('/Users/patrickkoch/projects/nuclear-fusion-at-home-workforce-alignment')
REPORT = json.loads((ROOT / 'coordination/logs/codex/calibration/20261016T053602Z/model/report.json').read_text())
SETTINGS = dict(multigrid_steps=deepcopy(pair.BASELINE_STEPS), max_threads=1,
                time_step=.5, n_poloidal_modes=10, max_toroidal_mode=10)


class Settings:
    def __init__(self, data):
        self.data = deepcopy(data)

    def model_dump(self, mode):
        return deepcopy(self.data)

    @classmethod
    def model_validate(cls, data):
        return cls(data)


def fixture(fail=False):
    factory = lambda boundary, settings: Settings(SETTINGS)
    module = SimpleNamespace(create_vmec_settings_from_preset=factory)
    calls = []

    def invoke(scorer, path):
        calls.append(path.name)
        path.mkdir(exist_ok=False)
        report = deepcopy(REPORT)
        for record in report['targets'].values():
            settings = module.create_vmec_settings_from_preset(None, settings=SimpleNamespace(
                fidelity='high_fidelity', multithreaded=False, verbose=False))
            record['vmec']['ns'] = settings.data['multigrid_steps'][-1]['n_flux_surfaces']
        (path / 'report.json').write_text(json.dumps(report))
        return 1 if fail else 0
    return module, factory, calls, invoke


class PairControls(unittest.TestCase):
    def run_fixture(self, output, fail=False):
        module, factory, calls, invoke = fixture(fail)
        original = pair.invoke
        pair.invoke = invoke
        try:
            result = pair.run_pair(None, module, output)
        finally:
            pair.invoke = original
            self.assertIs(module.create_vmec_settings_from_preset, factory)
        return result, calls

    def test_one_default_then_one_finer_invocation_and_bound_settings(self):
        with tempfile.TemporaryDirectory() as directory:
            result, calls = self.run_fixture(Path(directory))
            self.assertEqual(calls, ['default', 'model'])
            self.assertTrue(result['completed'])
            self.assertTrue(result['fresh_matched_baseline'])
            self.assertFalse(result['physical_admission'])
            for row in result['targets'].values():
                self.assertEqual(row['default_vmec']['ns'], 99)
                self.assertEqual(row['finer_vmec']['ns'], 199)
            # Tampering cannot bypass the unchanged pair-settings comparison.
            path = Path(directory) / 'default-effective-0.json'
            data = json.loads(path.read_text()); data['time_step'] = .25
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, 'captured default settings mismatch'):
                pair.paired_comparison(Path(directory))

    def test_failed_default_stops_before_finer_and_restores_factory(self):
        with tempfile.TemporaryDirectory() as directory:
            module, factory, calls, invoke = fixture(fail=True)
            original = pair.invoke; pair.invoke = invoke
            try:
                with self.assertRaisesRegex(ValueError, 'baseline incomplete'):
                    pair.run_pair(None, module, Path(directory))
                self.assertEqual(calls, ['default'])
                self.assertFalse((Path(directory) / 'finer').exists())
                self.assertIs(module.create_vmec_settings_from_preset, factory)
            finally:
                pair.invoke = original

    def test_reused_output_fails_before_second_invocation(self):
        with tempfile.TemporaryDirectory() as directory:
            self.run_fixture(Path(directory))
            with self.assertRaises(FileExistsError):
                self.run_fixture(Path(directory))

    def test_finer_report_tamper_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            self.run_fixture(Path(directory))
            path = Path(directory) / 'finer/model/report.json'
            path.write_text(path.read_text()+'\n')
            with self.assertRaisesRegex(ValueError, 'finer report hash mismatch'):
                pair.paired_comparison(Path(directory))


class ReservationControls(unittest.TestCase):
    def test_explicit_current_parent_window_and_no_silence_or_stale_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'notes').mkdir(); (root / 'automation').mkdir()
            now = datetime.now(timezone.utc)
            parent = '0491388c286cfd21872bd0da2ccaa8916c0366ed918879012c204cc189650bfc'
            def grant(start, end):
                return f'CAL-REQ-006 GRANTED manifest={parent} start={start.isoformat()} end={end.isoformat()}'
            current = grant(now-timedelta(minutes=1), now+timedelta(hours=1))
            expired = grant(now-timedelta(days=3), now-timedelta(days=2))
            text = 'No Claude native job runs in it\nCodex: #112 frozen radial study\n'
            peer = root / 'notes/claude.md'
            snapshot = root / 'automation/process-check.json'
            baseline = dict(checked_at=now.isoformat(), native_compute_pids=[],
                            controller_lock_held=True, other_codex_exec_worker=False)
            peer.write_text(text+current+'\n'+expired+'\n')
            snapshot.write_text(json.dumps(baseline))
            manifest = dict(coordination=str(root), reservation_manifest=parent)
            self.assertTrue(pair.reservation_check(manifest, 'a'*64)['inherited_task_reservation'])
            for altered in [dict(baseline, native_compute_pids=[123]),
                            dict(baseline, controller_lock_held=False),
                            dict(baseline, other_codex_exec_worker=True),
                            dict(baseline, checked_at=(now-timedelta(minutes=6)).isoformat())]:
                snapshot.write_text(json.dumps(altered))
                with self.assertRaises(ValueError):
                    pair.reservation_check(manifest, 'a'*64)
            snapshot.write_text(json.dumps(baseline))
            for invalid in [text+expired, current, text, text+current+'\n'+current]:
                peer.write_text(invalid)
                with self.assertRaises(ValueError):
                    pair.reservation_check(manifest, 'a'*64)


if __name__ == '__main__':
    unittest.main()
