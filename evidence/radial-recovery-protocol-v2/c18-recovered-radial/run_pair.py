"""Recovered-runtime ns99/ns199 pair. No scientific imports before live gates."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import importlib.util
import json
import re
import subprocess
from pathlib import Path
import sys
import time
import traceback

# All helpers are unchanged, hash-bound copies from the original radial protocol.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "c18-resolution-launcher"))
import launch_resolution as guard
import compare_resolution as comparison
from radial_settings_adapter import BASELINE_STEPS
from resolution_wrapper import run_finer


def reservation_check(manifest, digest):
    """Use the explicit current task reservation; retain its original identity."""
    coordination = Path(manifest["coordination"])
    peer_path = coordination / "notes/claude.md"
    peer = peer_path.read_text()
    now = datetime.now(timezone.utc)
    parent = manifest["reservation_manifest"]
    guard.need(parent == "0491388c286cfd21872bd0da2ccaa8916c0366ed918879012c204cc189650bfc",
               "unknown parent reservation")
    guard.need("No Claude native job runs in it" in peer and "Codex: #112 frozen radial study" in peer,
               "explicit free task-specific reservation required")
    pattern = rf"^CAL-REQ-006 GRANTED manifest={parent} start=(\S+) end=(\S+)$"
    current = []
    for line in peer.splitlines():
        found = re.fullmatch(pattern, line)
        if found:
            start, end = map(guard.timestamp, found.groups())
            if start <= now and (end - now).total_seconds() >= guard.LIMITS["wall_seconds"]:
                current.append(line)
    guard.need(len(current) == 1, "exactly one current task reservation required")
    snapshot_path = coordination / "automation/process-check.json"
    record = guard.check_live(parent, current[0], guard.load(snapshot_path), now,
                               (coordination / "automation/STOP").exists())
    record.update(recovery_manifest_sha256=digest, inherited_task_reservation=True,
                  peer_sha256=guard.sha(peer_path), controller_sha256=guard.sha(snapshot_path))
    return record


def invoke(scorer, output):
    sys.argv = [str(scorer.__file__), "--output", str(output)]
    return scorer.main()


@contextmanager
def capture_defaults(module, output):
    original = module.create_vmec_settings_from_preset
    recorded = []

    def create(boundary, settings):
        guard.need(settings.fidelity == "high_fidelity" and not settings.multithreaded
                   and not settings.verbose, "unchanged default preset required")
        model = original(boundary, settings=settings)
        data = model.model_dump(mode="json")
        guard.need(data["multigrid_steps"] == BASELINE_STEPS and data["max_threads"] == 1,
                   "unexpected default radial schedule/thread count")
        guard.need(len(recorded) < 2, "too many baseline settings calls")
        guard.write(output / f"default-effective-{len(recorded)}.json", data)
        recorded.append(data)
        return model

    module.create_vmec_settings_from_preset = create
    try:
        yield recorded
    finally:
        module.create_vmec_settings_from_preset = original


def paired_comparison(output):
    """Verify fresh reports/settings, then use the unchanged numerical verifier."""
    baseline_path = output / "default/report.json"
    finer = output / "finer"
    wrapper = comparison.strict_load(finer / "wrapper-result.json")
    guard.need(wrapper["completed"] is True and wrapper["scorer_exit_code"] == 0,
               "finer wrapper incomplete")
    guard.need(wrapper["targets"] == list(comparison.TARGETS)
               and wrapper["radial_only"] is True and wrapper["physical_admission"] is False,
               "wrapper scope mismatch")
    report_path = finer / "model/report.json"
    guard.need(guard.sha(report_path) == wrapper["report_sha256"], "finer report hash mismatch")
    entries = wrapper["effective_settings"]
    guard.need(len(entries) == 2, "exactly two finer settings records required")
    settings = []
    for index, entry in enumerate(entries):
        guard.need(entry["path"] == f"effective-settings-{index}.json", "settings path mismatch")
        path = finer / entry["path"]
        guard.need(guard.sha(path) == entry["sha256"], "finer settings hash mismatch")
        record = comparison.strict_load(path)
        guard.need(record["baseline_effective_settings"] == comparison.strict_load(
            output / f"default-effective-{index}.json"), "captured default settings mismatch")
        settings.append(record)
    result = comparison.compare_reports(comparison.strict_load(baseline_path),
                                        comparison.strict_load(report_path), settings)
    result["fresh_matched_baseline"] = True
    result["artifact_sha256"] = {str(path.relative_to(output)): guard.sha(path) for path in [
        baseline_path, report_path, finer / "wrapper-result.json",
        *sorted(output.glob("default-effective-*.json")),
        *sorted(finer.glob("effective-settings-*.json"))]}
    return result


def run_pair(scorer, module, output):
    """Four serial calls through two scorer invocations; never retry a failure."""
    with capture_defaults(module, output) as settings:
        code = invoke(scorer, output / "default")
    guard.need(code == 0 and len(settings) == 2, "rebuilt-runtime baseline incomplete")
    baseline = comparison.strict_load(output / "default/report.json")
    guard.need(tuple(baseline["targets"]) == comparison.TARGETS, "baseline target mismatch")
    for target in comparison.TARGETS:
        comparison.validate_record(baseline["targets"][target], target, 99)
    guard.write(output / "default-complete.json", {"report_sha256": guard.sha(
        output / "default/report.json"), "completed": True, "physical_admission": False})
    result = run_finer(lambda path: invoke(scorer, path), module, output / "finer")
    guard.need(result["completed"] is True, "finer execution incomplete")
    return paired_comparison(output)


def child(manifest, digest):
    guard.verify_runtime(manifest)
    for path, expected in manifest["files_sha256"].items():
        guard.need(guard.sha(path) == expected, f"child identity mismatch: {path}")
    coordination = Path(manifest["coordination"])
    reservation_check(manifest, digest)
    output = Path(manifest["output"])
    guard.need((output / "preflight.json").is_file(), "parent preflight missing")
    with (output / "child-started.json").open("x") as stream:
        json.dump({"manifest_sha256": digest}, stream)
    guard.write(output / "environment.json", manifest["environment"])
    # Scientific imports start only here, after identity and ownership checks.
    from constellaration.mhd import vmec_settings
    spec = importlib.util.spec_from_file_location("recovered_radial_scorer", manifest["scorer"])
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    result = run_pair(scorer, vmec_settings, output)
    guard.write(output / "comparison.json", result)
    prior = comparison.strict_load(manifest["historical_baseline"])
    current = comparison.strict_load(output / "default/report.json")
    drift = {"interpretation": "descriptive rebuilt-runtime bridge; no parity tolerance", "targets": {}}
    for target in comparison.TARGETS:
        old, new = prior["targets"][target], current["targets"][target]
        drift["targets"][target] = {"metrics_exact": old["metrics"] == new["metrics"],
            "settings_exact": old["settings"] == new["settings"],
            "benchmarks_exact": old["benchmarks"] == new["benchmarks"],
            "metric_signed_deltas": {key: new["metrics"][key] - value
                                     for key, value in old["metrics"].items()}}
    guard.write(output / "historical-baseline-drift.json", drift)


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--manifest-sha256", required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--execute", action="store_true")
    mode.add_argument("--child", action="store_true")
    args = parser.parse_args()
    guard.need(guard.sha(args.manifest) == args.manifest_sha256, "manifest hash mismatch")
    manifest = guard.load(args.manifest)
    if args.child:
        child(manifest, args.manifest_sha256)
        return 0
    source = manifest["source"]
    head = subprocess.check_output(["git", "-C", source, "rev-parse", "HEAD"], text=True).strip()
    dirty = subprocess.check_output(["git", "-C", source, "status", "--porcelain"], text=True).strip()
    guard.verify_files(manifest, head, dirty)
    record = reservation_check(manifest, args.manifest_sha256)
    if not args.execute:
        print(json.dumps({"preflight": record, "native_started": False}))
        return 0
    output = Path(manifest["output"])
    output.mkdir(exist_ok=False)
    for name in ("cache", "tmp"):
        (output / name).mkdir()
    guard.write(output / "preflight.json", record)
    command = [manifest["native_python"], "-B", str(Path(__file__).resolve()), "--manifest",
               str(args.manifest.resolve()), "--manifest-sha256", args.manifest_sha256, "--child"]
    outcome = {"completed": False, "physical_admission": False,
               "manifest_sha256": args.manifest_sha256}
    try:
        result = guard.supervise(command, output, guard.clean_environment(output),
            Path(manifest["coordination"]) / "automation/STOP",
            limits={**guard.LIMITS, "wall_seconds": min(1740, 1770 - (time.monotonic() - started))})
        outcome["execution"] = result
        guard.need(result["exit_code"] == 0 and result["stop_reason"] is None, "child incomplete")
        for path, expected in manifest["files_sha256"].items():
            guard.need(guard.sha(path) == expected, f"postflight identity mismatch: {path}")
        outcome["comparison_sha256"] = guard.sha(output / "comparison.json")
        guard.need(time.monotonic() - started < guard.LIMITS["wall_seconds"], "task deadline")
        outcome["completed"] = True
    except Exception:
        outcome["error"] = traceback.format_exc()
    finally:
        outcome["wall_seconds"] = time.monotonic() - started
        guard.write(output / "launch-result.json", outcome)
    return 0 if outcome["completed"] else 1


if __name__ == "__main__":
    sys.exit(main())
