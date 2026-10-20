"""One frozen #112 ns199 run. Default invocation performs no native work.

No scientific imports until child-side frozen identities and live gates pass.
The task-specific grant must bind the public manifest hash. Never reuse output.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata as metadata
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import time
import traceback


LIMITS = {"wall_seconds": 1800, "threads": 1, "output_bytes": 100 * 1024**2,
          "start_disk_reserve_bytes": 3 * 1024**3,
          "runtime_disk_reserve_bytes": 2 * 1024**3}
REQUEST = "CAL-REQ-006"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2, allow_nan=False) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def timestamp(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    need(result.tzinfo is not None, "timezone required")
    return result


def check_live(manifest_hash, peer_text, controller, now, stop=False):
    """Require a new, manifest-specific explicit grant; old windows never count."""
    need(not stop, "STOP present")
    grants = re.findall(
        rf"^{REQUEST} GRANTED manifest=([0-9a-f]{{64}}) start=(\S+) end=(\S+)$",
        peer_text, re.MULTILINE)
    matching = [(timestamp(start), timestamp(end)) for digest, start, end in grants
                if digest == manifest_hash]
    need(len(matching) == 1, "one explicit current manifest-specific CAL-REQ-006 grant required")
    start, end = matching[0]
    need(start <= now and (end - now).total_seconds() >= LIMITS["wall_seconds"],
         "grant is not current or lacks the full 1800-second window")
    age = (now - timestamp(controller["checked_at"])).total_seconds()
    need(0 <= age < 300, "controller inventory must be less than five minutes old")
    need(controller["native_compute_pids"] == [], "native inventory is not empty")
    need(controller["controller_lock_held"] is True
         and controller["other_codex_exec_worker"] is False, "controller ownership mismatch")
    return {"request": REQUEST, "manifest_sha256": manifest_hash,
            "grant_start": start.isoformat(), "grant_end": end.isoformat(),
            "controller_age_seconds": age, "controller": controller}


def verify_files(manifest, actual_head, dirty):
    need(manifest["limits"] == LIMITS, "frozen resource limits differ")
    need(actual_head == manifest["source_head"] and not dirty, "source revision/dirty mismatch")
    for path, digest in manifest["files_sha256"].items():
        need(sha(path) == digest, f"frozen file mismatch: {path}")
    need(not Path(manifest["output"]).exists(), "output already exists; no repeat permitted")
    need(shutil.disk_usage(Path(manifest["output"]).parent).free >= LIMITS["start_disk_reserve_bytes"],
         "3 GiB start disk reserve required")


def verify_runtime(manifest):
    """Metadata and byte reads only; run in the pinned child before imports."""
    expected = manifest["environment"]
    observed = {"python": sys.version, "platform": platform.platform(),
                "machine": platform.machine(),
                "versions": {name: metadata.version(name) for name in expected["versions"]}}
    need(observed == expected, "pinned runtime identity mismatch")
    return observed


def preflight(manifest, manifest_hash):
    source = Path(manifest["source"])
    head = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    dirty = subprocess.check_output(["git", "-C", str(source), "status", "--porcelain"], text=True).strip()
    verify_files(manifest, head, dirty)
    coordination = Path(manifest["coordination"])
    peer = coordination / "notes/claude.md"
    snapshot = coordination / "automation/process-check.json"
    record = check_live(manifest_hash, peer.read_text(encoding="utf-8"), load(snapshot),
                        datetime.now(timezone.utc), (coordination / "automation/STOP").exists())
    record.update(peer_sha256=sha(peer), controller_sha256=sha(snapshot))
    return record


def clean_environment(output):
    """Allowlisted environment; caches/output owned by this single run."""
    return {"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1",
            "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1",
            "VECLIB_MAXIMUM_THREADS": "1", "NUMEXPR_NUM_THREADS": "1",
            "XDG_CACHE_HOME": str(output / "cache"),
            "MPLCONFIGDIR": str(output / "cache/matplotlib"), "TMPDIR": str(output / "tmp")}


def supervise(command, output, env, stop_path, *, limits=None):
    """Monitor only the child launched here and this run's output files."""
    limits = LIMITS if limits is None else limits
    started = time.monotonic()
    reason = None
    with (output / "native.stdout").open("xb") as stdout, (output / "native.stderr").open("xb") as stderr:
        child = subprocess.Popen(command, env=env, cwd=output, stdout=stdout, stderr=stderr)
        try:
            while child.poll() is None:
                size = sum(p.stat().st_size for p in output.rglob("*") if p.is_file())
                if time.monotonic() - started >= limits["wall_seconds"]:
                    reason = "wall limit"
                elif shutil.disk_usage(output).free < limits["runtime_disk_reserve_bytes"]:
                    reason = "runtime disk reserve"
                elif size >= limits["output_bytes"]:
                    reason = "output size limit"
                elif stop_path.exists():
                    reason = "STOP present"
                if reason:
                    child.terminate()
                    child.wait(timeout=10)
                    break
                time.sleep(.2)
        finally:
            if child.poll() is None:
                child.terminate()
                child.wait(timeout=10)
    result = {"exit_code": child.returncode, "stop_reason": reason,
              "wall_seconds": time.monotonic() - started,
              "output_bytes": sum(p.stat().st_size for p in output.rglob("*") if p.is_file()),
              "finished_at": datetime.now(timezone.utc).isoformat()}
    write(output / "execution-result.json", result)
    return result


def child_main(manifest_path, digest):
    need(sha(manifest_path) == digest, "manifest hash mismatch")
    manifest = load(manifest_path)
    verify_runtime(manifest)
    # Parent created the exclusive run root. Recheck every byte and live gate,
    # without the parent-only output-absence check.
    for path, expected in manifest["files_sha256"].items():
        need(sha(path) == expected, f"child frozen file mismatch: {path}")
    coordination = Path(manifest["coordination"])
    check_live(digest, (coordination / "notes/claude.md").read_text(encoding="utf-8"),
               load(coordination / "automation/process-check.json"), datetime.now(timezone.utc),
               (coordination / "automation/STOP").exists())
    output = Path(manifest["output"])
    need(output.is_dir() and (output / "preflight.json").is_file(), "parent preflight record missing")
    need(not (output / "finer").exists(), "finer output already exists; no repeat permitted")
    # An exclusive child marker also preserves startup failures and bars retries.
    with (output / "child-started.json").open("x", encoding="utf-8") as stream:
        stream.write(json.dumps({"manifest_sha256": digest,
                                 "started_at": datetime.now(timezone.utc).isoformat()}) + "\n")
    write(output / "environment.json", manifest["environment"])
    # All imports below are reached only in --execute's supervised native child.
    sys.path.insert(0, manifest["harness"])
    from resolution_wrapper import run_finer
    from constellaration.mhd import vmec_settings
    spec = importlib.util.spec_from_file_location("frozen_radial_scorer", manifest["scorer"])
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)

    def invoke(model_output):
        sys.argv = [manifest["scorer"], "--output", str(model_output)]
        return scorer.main()

    result = run_finer(invoke, vmec_settings, output / "finer")
    return 0 if result["completed"] else 1


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--manifest-sha256", required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--execute", action="store_true")
    mode.add_argument("--child", action="store_true")
    args = parser.parse_args()
    need(sha(args.manifest) == args.manifest_sha256, "manifest hash mismatch")
    if args.child:
        return child_main(args.manifest, args.manifest_sha256)
    manifest = load(args.manifest)
    # Default readiness check cannot spawn a scientific child.
    record = preflight(manifest, args.manifest_sha256)
    if not args.execute:
        print(json.dumps({"preflight": record, "native_started": False}))
        return 0
    output = Path(manifest["output"])
    output.mkdir(exist_ok=False)
    (output / "cache").mkdir()
    (output / "tmp").mkdir()
    write(output / "preflight.json", record)
    command = [manifest["native_python"], "-B", str(Path(__file__).resolve()),
               "--manifest", str(args.manifest.resolve()),
               "--manifest-sha256", args.manifest_sha256, "--child"]
    # Reserve sixty seconds for metadata checks, startup and final comparison.
    # The external dispatch still has its absolute 1800-second task ceiling.
    outcome = {"completed": False, "physical_admission": False,
               "manifest_sha256": args.manifest_sha256}
    try:
        remaining = min(1740, LIMITS["wall_seconds"] - (time.monotonic() - started) - 30)
        need(remaining > 0, "preflight exhausted task deadline")
        result = supervise(command, output, clean_environment(output),
                           Path(manifest["coordination"]) / "automation/STOP",
                           limits={**LIMITS, "wall_seconds": remaining})
        outcome["execution"] = result
        for path, expected in manifest["files_sha256"].items():
            need(sha(path) == expected, f"postflight frozen file mismatch: {path}")
        need(result["exit_code"] == 0 and result["stop_reason"] is None, "native child incomplete")
        sys.path.insert(0, manifest["comparison_harness"])
        from compare_resolution import compare_files
        comparison = compare_files(manifest["baseline"], output / "finer")
        write(output / "comparison.json", comparison)
        outcome["comparison_sha256"] = sha(output / "comparison.json")
        need(time.monotonic() - started < LIMITS["wall_seconds"], "task deadline exceeded")
        outcome["completed"] = True
    except Exception:
        outcome["error"] = traceback.format_exc()
    finally:
        outcome["wall_seconds"] = time.monotonic() - started
        write(output / "launch-result.json", outcome)
    return 0 if outcome["completed"] else 1


if __name__ == "__main__":
    sys.exit(main())
