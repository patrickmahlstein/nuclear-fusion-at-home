"""Software-only radial comparison; no solver imports or acceptance tolerance.

The CLI requires a future frozen run manifest. This is not a native launcher.
Never use synthetic test reports as scientific evidence.
"""
import argparse
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path


TARGETS = ("reference401", "selected401")
METRICS = ("vacuum_well", "flux_compression_in_regions_of_bad_curvature",
           "minimum_normalized_magnetic_gradient_scale_length", "qi")
BASELINE_SHA256 = "8d8afa15ed92ae7814638029d68916875bdebfe30c28c0f2525b033b5871ccf1"
INPUTS = {
    "reference401": "57394ef682f3c6399faa03012abc02da2eb1ce40703a4f99640ece3d07e5691f",
    "selected401": "6bec3483eaced499bafe7ee94b16aa960d219ec1fec86cc0690012f8ebdb033e",
}
BENCHMARKS = ("geometrical", "simple_to_build_qi", "mhd_stable_qi")
OFFICIAL_RELATIVE_TOLERANCE = .01  # unchanged pinned problems.py rule


def need(condition, message):
    if not condition:
        raise ValueError(message)


def number(value):
    need(type(value) in (int, float) and math.isfinite(value), "finite number required")
    return value


def strict_load(path):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def constant(value):
        raise ValueError(f"nonfinite JSON constant: {value}")

    return json.loads(Path(path).read_text(), object_pairs_hook=pairs,
                      parse_constant=constant)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate_record(record, target, ns):
    need(record["completed"] is True, f"incomplete target: {target}")
    need(record["input_sha256"] == INPUTS[target], "input identity mismatch")
    need(record["conversion_validation"]["passed"] is True, "conversion failure")
    r00 = number(record["conversion"]["R00"])
    need(r00 > 0, "positive R00 required")
    need(number(record["conversion"]["max_abs_difference_to_vmecpp_reader"]) == 0,
         "reader mismatch")
    need(record["geometry_check"]["grid"] == [64, 128], "geometry grid mismatch")
    for key in ("surface_vs_input", "surface_coefficient_bound",
                "vmec_boundary_coefficient_bound", "vmec_boundary_vs_input"):
        residual = number(record["geometry_check"][key])
        need(0 <= residual <= 1e-10 * r00, "geometry residual outside existing gate")
    vmec = record["vmec"]
    need((vmec["ns"], vmec["mpol"], vmec["ntor"], vmec["ier_flag"])
         == (ns, 10, 10, 0), "VMEC grid or convergence flag mismatch")
    for key in ("fsqr", "fsqz", "fsql"):
        need(number(vmec[key]) >= 0, "invalid convergence residual")
    need(number(record["forward_model_seconds"]) >= 0, "invalid runtime")
    for value in record["metrics"].values():
        number(value)
    need(set(record["benchmarks"]) == set(BENCHMARKS), "benchmark set mismatch")
    for benchmark in record["benchmarks"].values():
        violations = benchmark["normalized_violations"]
        need(violations and type(benchmark["feasible"]) is bool, "invalid benchmark")
        for value in violations:
            number(value)
        need(benchmark["feasible"] == all(x <= OFFICIAL_RELATIVE_TOLERANCE for x in violations),
             "benchmark feasibility/violation mismatch")
        for key, value in benchmark.items():
            if key != "feasible":
                for item in value if isinstance(value, list) else [value]:
                    number(item)


def compare_reports(baseline, finer, settings):
    """Validate matching reports and return descriptive differences only."""
    need(tuple(baseline["targets"]) == TARGETS == tuple(finer["targets"]),
         "target set/order mismatch")
    need(baseline["versions"] == finer["versions"], "environment version mismatch")
    need(baseline["threads"] == finer["threads"], "thread settings mismatch")
    for key in ("kind", "python", "platform", "machine", "geometry_relative_tolerance",
                "boundary_only"):
        need(baseline[key] == finer[key], f"report metadata mismatch: {key}")
    need(baseline["physical_admission"] is False and finer["physical_admission"] is False,
         "unexpected physical admission")
    need(len(settings) == len(TARGETS), "one settings record per target required")
    result = {"completed": True, "physical_admission": False, "radial_only": True,
              "interpretation": "Two radial settings do not establish convergence, total numerical uncertainty or scorer qualification. No new sensitivity pass/fail tolerance is applied. Official feasibility retains its normalized 0.01 tolerance; strict-bound crossings are separate diagnostics.",
              "targets": {}}
    for index, target in enumerate(TARGETS):
        before, after = baseline["targets"][target], finer["targets"][target]
        validate_record(before, target, 99)
        validate_record(after, target, 199)
        need(before["settings"] == after["settings"], "high-level settings mismatch")
        entry = settings[index]
        old, new = entry["baseline_effective_settings"], entry["finer_effective_settings"]
        expected = deepcopy(old)
        need([s["n_flux_surfaces"] for s in old["multigrid_steps"]] == [25, 51, 99],
             "unexpected baseline radial schedule")
        expected["multigrid_steps"][-1]["n_flux_surfaces"] = 199
        need(new == expected, "effective settings changed beyond final radial grid")
        need(old["max_threads"] == 1 and old["n_poloidal_modes"] == old["max_toroidal_mode"] == 10,
             "unexpected baseline effective settings")
        deltas = {}
        for metric in METRICS:
            a, b = number(before["metrics"][metric]), number(after["metrics"][metric])
            delta = number(b - a)
            deltas[metric] = {"default": a, "finer": b, "signed_delta": delta,
                              "absolute_delta": abs(delta),
                              "absolute_relative_delta": number(abs(delta) / abs(a)) if a else None}
            if metric == "qi":
                deltas[metric]["default_log10"] = math.log10(a) if a > 0 else None
                deltas[metric]["finer_log10"] = math.log10(b) if b > 0 else None
        benchmarks = {}
        for name in BENCHMARKS:
            a, b = before["benchmarks"][name], after["benchmarks"][name]
            need(set(a) == set(b), "benchmark schema mismatch")
            va, vb = a["normalized_violations"], b["normalized_violations"]
            need(len(va) == len(vb), "benchmark residual count mismatch")
            benchmarks[name] = {"default": deepcopy(a), "finer": deepcopy(b),
                                "feasibility_changed": a["feasible"] != b["feasible"],
                                "strict_component_bound_crossings": [
                                    {"index": i, "default_pass": x <= 0, "finer_pass": y <= 0}
                                    for i, (x, y) in enumerate(zip(va, vb)) if (x <= 0) != (y <= 0)],
                                "official_component_tolerance_crossings": [
                                    {"index": i, "default_pass": x <= OFFICIAL_RELATIVE_TOLERANCE,
                                     "finer_pass": y <= OFFICIAL_RELATIVE_TOLERANCE}
                                    for i, (x, y) in enumerate(zip(va, vb))
                                    if (x <= OFFICIAL_RELATIVE_TOLERANCE) != (y <= OFFICIAL_RELATIVE_TOLERANCE)]}
        result["targets"][target] = {
            "metrics": deltas, "benchmarks": benchmarks,
            "default_vmec": deepcopy(before["vmec"]), "finer_vmec": deepcopy(after["vmec"]),
            "default_seconds": before["forward_model_seconds"],
            "finer_seconds": after["forward_model_seconds"],
            "default_geometry": deepcopy(before["geometry_check"]),
            "finer_geometry": deepcopy(after["geometry_check"])}
    return result


def compare_files(baseline_path, run_root):
    """Bind report/settings bytes to completed wrapper output before comparison.

    Full source/environment/runner identities still belong in the future launcher
    manifest. These hashes detect substitution, not authenticity or public freeze.
    """
    root = Path(run_root)
    need(sha(baseline_path) == BASELINE_SHA256, "frozen baseline hash mismatch")
    wrapper_path = root / "wrapper-result.json"
    wrapper = strict_load(wrapper_path)
    need(wrapper["completed"] is True and wrapper["scorer_exit_code"] == 0,
         "wrapper incomplete")
    need(wrapper["targets"] == list(TARGETS) and wrapper["radial_only"] is True
         and wrapper["physical_admission"] is False, "wrapper scope mismatch")
    report_path = root / "model/report.json"
    need(sha(report_path) == wrapper["report_sha256"], "finer report hash mismatch")
    entries = wrapper["effective_settings"]
    need(len(entries) == len(TARGETS), "settings count mismatch")
    settings = []
    identities = {"baseline_report": sha(baseline_path), "finer_report": sha(report_path),
                  "wrapper_result": sha(wrapper_path), "effective_settings": []}
    for index, entry in enumerate(entries):
        need(entry["path"] == f"effective-settings-{index}.json", "settings path mismatch")
        path = root / entry["path"]
        need(sha(path) == entry["sha256"], "effective settings hash mismatch")
        settings.append(strict_load(path))
        identities["effective_settings"].append(sha(path))
    result = compare_reports(strict_load(baseline_path), strict_load(report_path), settings)
    result["artifact_sha256"] = identities
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = compare_files(args.baseline, args.run_root)
    # Exclusive output prevents replacing a prior comparison or failure.
    with args.output.open("x") as stream:
        stream.write(json.dumps(result, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
