"""Live-gate and owned-stub supervisor tests. Never launch a solver."""
from datetime import datetime, timedelta, timezone
from copy import deepcopy
import importlib.abc
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

FORBIDDEN = {"constellaration", "vmecpp", "numpy", "scipy", "jax", "jaxlib", "simsopt", "desc"}


class NoScientificImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in FORBIDDEN:
            raise AssertionError(f"scientific import forbidden: {fullname}")
        return None


sys.meta_path.insert(0, NoScientificImports())
import launch_resolution as launch


class LaunchTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 16, 18, 0, tzinfo=timezone.utc)
        self.digest = "a" * 64
        self.peer = f"CAL-REQ-006 GRANTED manifest={self.digest} start=2026-10-16T18:00Z end=2026-10-16T19:00Z"
        self.controller = {"checked_at": self.now.isoformat(), "native_compute_pids": [],
                           "controller_lock_held": True, "other_codex_exec_worker": False}

    def check(self, **change):
        values = {"manifest_hash": self.digest, "peer_text": self.peer,
                  "controller": self.controller, "now": self.now}
        return launch.check_live(**{**values, **change})

    def test_only_manifest_specific_new_grant_counts(self):
        self.assertEqual(self.check()["request"], "CAL-REQ-006")
        for text in ("", self.peer.replace("006", "005"), self.peer.replace(self.digest, "b" * 64),
                     self.peer + "\n" + self.peer):
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.check(peer_text=text)

    def test_not_yet_current_expired_and_insufficient_window_rejected(self):
        for offset in (-1, 1801, 3601):
            with self.subTest(offset=offset), self.assertRaisesRegex(ValueError, "not current"):
                self.check(now=self.now + timedelta(seconds=offset))

    def test_snapshot_age_empty_inventory_and_ownership(self):
        for change in ({"checked_at": (self.now - timedelta(seconds=300)).isoformat()},
                       {"checked_at": (self.now + timedelta(seconds=1)).isoformat()},
                       {"native_compute_pids": [123]}, {"controller_lock_held": False},
                       {"other_codex_exec_worker": True}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.check(controller={**self.controller, **change})
        with self.assertRaisesRegex(ValueError, "STOP present"):
            self.check(stop=True)

    def test_timezone_required(self):
        with self.assertRaisesRegex(ValueError, "timezone required"):
            launch.timestamp("2026-10-16T18:00:00")

    def fixture(self, directory):
        root = Path(directory)
        source = root / "input.json"
        source.write_text("{}", encoding="utf-8")
        return {"limits": deepcopy(launch.LIMITS), "source_head": "fixed",
                "files_sha256": {str(source): launch.sha(source)}, "output": str(root / "new")}

    def test_frozen_files_source_and_output_checks(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.fixture(directory)
            launch.verify_files(manifest, "fixed", False)
            for head, dirty in (("other", False), ("fixed", True)):
                with self.assertRaisesRegex(ValueError, "source revision"):
                    launch.verify_files(manifest, head, dirty)
            Path(manifest["output"]).mkdir()
            with self.assertRaisesRegex(ValueError, "output already exists"):
                launch.verify_files(manifest, "fixed", False)
            Path(manifest["output"]).rmdir()
            Path(next(iter(manifest["files_sha256"]))).write_text("changed", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "frozen file mismatch"):
                launch.verify_files(manifest, "fixed", False)

    def test_resource_limits_cannot_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.fixture(directory)
            manifest["limits"]["threads"] = 2
            with self.assertRaisesRegex(ValueError, "resource limits differ"):
                launch.verify_files(manifest, "fixed", False)

    def test_runtime_metadata_mismatch_precedes_imports(self):
        expected = {"python": sys.version, "platform": launch.platform.platform(),
                    "machine": launch.platform.machine(), "versions": {"example": "1"}}
        with patch.object(launch.metadata, "version", return_value="1"):
            self.assertEqual(launch.verify_runtime({"environment": expected}), expected)
        with patch.object(launch.metadata, "version", return_value="2"):
            with self.assertRaisesRegex(ValueError, "runtime identity mismatch"):
                launch.verify_runtime({"environment": expected})
        self.assertFalse(FORBIDDEN.intersection(sys.modules))

    def test_clean_environment_does_not_forward_credentials(self):
        env = launch.clean_environment(Path("/owned/run"))
        self.assertNotIn("HOME", env)
        self.assertNotIn("PYTHONPATH", env)
        self.assertEqual(env["OMP_NUM_THREADS"], "1")
        self.assertEqual(env["XDG_CACHE_HOME"], "/owned/run/cache")

    def stub(self, root, code, **limits):
        return launch.supervise([sys.executable, "-I", "-S", "-B", "-c", code], root,
                                launch.clean_environment(root), root / "STOP",
                                limits={**launch.LIMITS, **limits})

    def test_supervisor_success_preserves_stdout_and_result(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.stub(root, "print('harmless stub')")
            self.assertEqual(result["exit_code"], 0)
            self.assertIsNone(result["stop_reason"])
            self.assertEqual((root / "native.stdout").read_text().strip(), "harmless stub")
            self.assertEqual(launch.load(root / "execution-result.json"), result)

    def test_supervisor_wall_output_disk_and_stop_limits(self):
        for name in ("wall", "output", "disk", "stop"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                changes = {}
                if name == "wall":
                    changes["wall_seconds"] = .01
                elif name == "output":
                    changes["output_bytes"] = 0
                elif name == "disk":
                    changes["runtime_disk_reserve_bytes"] = 10**30
                else:
                    (root / "STOP").touch()
                result = self.stub(root, "import time; time.sleep(5)", **changes)
                self.assertNotEqual(result["exit_code"], 0)
                self.assertEqual(result["stop_reason"], {"wall": "wall limit", "output": "output size limit",
                                 "disk": "runtime disk reserve", "stop": "STOP present"}[name])

    def test_child_denies_without_grant_before_scientific_import(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "notes").mkdir()
            (root / "automation").mkdir()
            (root / "notes/claude.md").write_text("No grant", encoding="utf-8")
            launch.write(root / "automation/process-check.json", self.controller)
            manifest = {"coordination": str(root), "files_sha256": {}, "environment": {}}
            path = root / "manifest.json"
            launch.write(path, manifest)
            with patch.object(launch, "verify_runtime", return_value={}):
                with self.assertRaisesRegex(ValueError, "CAL-REQ-006 grant required"):
                    launch.child_main(path, launch.sha(path))
            self.assertFalse(FORBIDDEN.intersection(sys.modules))


if __name__ == "__main__":
    unittest.main(verbosity=2)
