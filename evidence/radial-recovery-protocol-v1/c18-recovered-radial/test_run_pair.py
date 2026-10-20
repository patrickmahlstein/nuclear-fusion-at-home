"""Software controls: no model imports or scientific calculations."""
from copy import deepcopy
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


if __name__ == '__main__':
    unittest.main()
