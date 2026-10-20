"""Isolated resolution wrapper, not a native launcher or authorization gate.

A future dedicated launcher must verify frozen identities, versions, resource
limits and current task-specific handoff BEFORE importing any scientific module.
This module imports no scientific package and never changes the approved scorer.
"""
import hashlib
import json
import os
from pathlib import Path
import traceback

from radial_settings_adapter import radial_override


TARGETS = ("reference401", "selected401")


def write_json(path, value):
    """Publish a complete strict-JSON artifact; write failures propagate."""
    raw = (json.dumps(value, indent=2, allow_nan=False) + "\n").encode()
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def run_finer(scorer_main, vmec_settings_module, output):
    """Call unchanged scorer main once, with an exclusive output root.

scorer_main(model_output) must invoke approved main with --output model_output,
no --confirm/custom input, and return its exit code. The future launcher supplies
that verified callback. Failed/incomplete runs remain evidence and are not retried.
"""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    records = []
    result = {"completed": False, "targets": list(TARGETS),
              "radial_only": True, "physical_admission": False,
              "effective_settings": []}

    def record_settings(record):
        if len(records) >= len(TARGETS):
            raise ValueError("too many settings factory calls")
        path = output / f"effective-settings-{len(records)}.json"
        write_json(path, record)
        # Read the strict serialized representation that downstream readers use.
        records.append(json.loads(path.read_text()))
        result["effective_settings"].append({
            "path": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})

    try:
        with radial_override(vmec_settings_module, record_settings):
            result["scorer_exit_code"] = scorer_main(output / "model")
        report_path = output / "model/report.json"
        result["report_sha256"] = hashlib.sha256(report_path.read_bytes()).hexdigest()
        report = json.loads(report_path.read_text())
        if tuple(report["targets"]) != TARGETS:
            raise ValueError("unexpected scorer target order or identity")
        if result["scorer_exit_code"] != 0:
            raise ValueError("scorer reported failure; partial records retained")
        if len(records) != len(TARGETS):
            raise ValueError("one effective settings record per target required")
        for target in TARGETS:
            record = report["targets"][target]
            if not record.get("completed") or record.get("vmec", {}).get("ns") != 199:
                raise ValueError(f"incomplete target or unexpected final radial grid: {target}")
            if not record.get("conversion_validation", {}).get("passed"):
                raise ValueError(f"geometry validation did not pass: {target}")
        result["completed"] = True
    except Exception:
        result["error"] = traceback.format_exc()
    finally:
        write_json(output / "wrapper-result.json", result)
    return result
