"""N26: ConStellaration's DESC omnigenity pipeline on a dataset row, optionally adding MagneticWell >= 0 and
Elongation <= cap, then scored with the high-fidelity forward model. argv: row.json out.json arm(ctrl|well) [cap]"""
import json, math, sys, time
import numpy as np
from constellaration.data_generation import desc_optimization as dopt, desc_optimization_settings as dset
from constellaration.omnigeneity import omnigenity_field_sampling as ofs, omnigenity_field_desc
from constellaration.geometry import surface_utils_desc
import constellaration.forward_model as fm, constellaration.problems as problems
import desc.objectives as dobj

def main():
    rec = json.load(open(sys.argv[1])); out = sys.argv[2]; arm = sys.argv[3]; cap = float(sys.argv[4]) if len(sys.argv) > 4 else 4.5
    targets = ofs.OmnigenousFieldAndTargets.model_validate(rec["omnigenous_field_and_targets.json"])
    settings = dset.DescOmnigenousFieldOptimizationSettings.model_validate(rec["desc_omnigenous_field_optimization_settings.json"])
    t0 = time.time()
    surf = dopt.generate_nae_initialization_from_targets(targets=targets, settings=settings.initial_guess_settings) \
        if isinstance(settings.initial_guess_settings, dset.NearAxisExpansionInitialGuessSettings) else \
        dopt.generate_qp_initialization_from_targets(targets=targets, settings=settings.initial_guess_settings)
    eq = dopt.solve_desc_equilibrium(dopt.create_desc_equilibrium_object(surf, settings.equilibrium_settings))
    obj = dopt.create_desc_objective_function(eq, targets, settings.objective_settings)
    if arm == "well":
        objs = list(obj.objectives)
        objs.append(dobj.MagneticWell(eq=eq, bounds=(0.0, np.inf), weight=10.0))
        objs.append(dobj.Elongation(eq=eq, bounds=(0.0, cap), weight=1.0))
        obj = dobj.ObjectiveFunction(tuple(objs))
    opt = dopt.create_desc_optimizer(settings.optimizer_settings)
    (eq,), _ = opt.optimize(things=eq, objective=obj, constraints=dopt.create_desc_constraints(eq),
                            maxiter=settings.optimizer_settings.maxiter, verbose=1)
    eq = dopt.solve_desc_equilibrium(eq)
    b = surface_utils_desc.from_desc_fourier_rz_toroidal_surface(eq.surface)
    res = dict(row=rec["row"], arm=arm, cap=cap, desc_seconds=time.time()-t0, boundary=json.loads(b.model_dump_json()))
    try:
        m, _ = fm.forward_model(b, settings=fm.ConstellarationSettings.default_high_fidelity())
        res["metrics"] = json.loads(m.model_dump_json())
        res["mhd_stable_feasibility"] = float(problems.MHDStableQIStellarator().compute_feasibility(m))
    except Exception as e:
        res["forward_error"] = repr(e)
    res["stored_metrics"] = rec["metrics.json"]
    json.dump(res, open(out, "w"))
    m = res.get("metrics")
    if m: print(arm, rec["row"], f"feas {res['mhd_stable_feasibility']:.3f} A {m['aspect_ratio']:.2f} log10QI {math.log10(m['qi']):.2f} "
                f"FC {m['flux_compression_in_regions_of_bad_curvature']:.3f} W {m['vacuum_well']:.4f} mirror {m['edge_magnetic_mirror_ratio']:.3f} "
                f"iota {m['edge_rotational_transform_over_n_field_periods']:.3f} elong {m['max_elongation']:.2f} LgradB {m['minimum_normalized_magnetic_gradient_scale_length']:.2f} t {res['desc_seconds']:.0f}s")

if __name__ == "__main__":
    main()
