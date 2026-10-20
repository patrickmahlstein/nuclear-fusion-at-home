"""Process-local ns99 -> ns199 adapter for the frozen #112 radial study.

No scientific imports. This adapter does not run a model or change scoring.
The future runner must verify source/environment identities before installation.
"""

from contextlib import contextmanager
from copy import deepcopy


BASELINE_STEPS = [
    {"n_flux_surfaces": 25, "force_tolerance": 1e-17, "n_max_iterations": 2000},
    {"n_flux_surfaces": 51, "force_tolerance": 1e-17, "n_max_iterations": 2000},
    {"n_flux_surfaces": 99, "force_tolerance": 1e-15, "n_max_iterations": 40000},
]


def refine_radially(original):
    """Return a validated independent settings model with exactly one leaf changed."""
    before = original.model_dump(mode="python")
    if before.get("multigrid_steps") != BASELINE_STEPS:
        raise ValueError("unexpected baseline multigrid schedule")
    if before.get("max_threads") != 1 or before.get("time_step") != 0.5:
        raise ValueError("unexpected baseline thread count or time step")
    expected = deepcopy(before)
    expected["multigrid_steps"][-1]["n_flux_surfaces"] = 199
    refined = type(original).model_validate(expected)
    if refined.model_dump(mode="python") != expected:
        raise ValueError("settings validation changed the radial-only override")
    if original.model_dump(mode="python") != before:
        raise ValueError("settings validation mutated the baseline")
    return refined, {"baseline_effective_settings": before,
                     "finer_effective_settings": deepcopy(expected)}


@contextmanager
def radial_override(vmec_settings_module, record_settings):
    """Intercept the pinned forward model's factory, restoring it on every exit.

    record_settings must persist effective settings before returning. Exceptions
    propagate, so a record failure stops the caller before a VMEC invocation.
    Use only in the future single-threaded dedicated resolution subprocess.
    """
    original_factory = vmec_settings_module.create_vmec_settings_from_preset
    if getattr(original_factory, "_c18_radial_override", False):
        raise ValueError("nested radial override is not allowed")

    def create(boundary, settings):
        if (settings.fidelity != "high_fidelity" or settings.multithreaded
                or settings.verbose):
            raise ValueError("unchanged single-thread high-fidelity preset required")
        baseline = original_factory(boundary, settings=settings)
        refined, record = refine_radially(baseline)
        record_settings(record)
        return refined

    create._c18_radial_override = True
    vmec_settings_module.create_vmec_settings_from_preset = create
    try:
        yield
    finally:
        vmec_settings_module.create_vmec_settings_from_preset = original_factory
