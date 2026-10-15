import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import alm_log24 as alm_log
import constellaration.forward_model as fm, constellaration.initial_guess as init
import constellaration.optimization.augmented_lagrangian as al
import constellaration.optimization.augmented_lagrangian_runner as runner
import constellaration.optimization.settings as os_
import constellaration.problems as problems, constellaration.utils.seed_util as seed_util
from constellaration.mhd import vmec_settings as vs
from constellaration.geometry import surface_rz_fourier as srf
import numpy as np


def main():
    arm, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True); os.environ["N23_LOG"] = out
    runner.objective_constraints = alm_log.objective_constraints_logged
    SET = os_.OptimizationSettings(max_poloidal_mode=4, max_toroidal_mode=4, infinity_norm_spectrum_scaling=1.5,
        optimizer_settings=os_.AugmentedLagrangianMethodSettings(maxit=10,
            oracle_settings=os_.NevergradSettings(num_workers=6, budget_initial=800, budget_max=20000,
                                                  budget_increment=100, max_time=None, batch_mode=False),
            penalty_parameters_initial=10, bounds_initial=0.33,
            augmented_lagrangian_settings=al.AugmentedLagrangianSettings(constraint_violation_tolerance_reduction_factor=0.8,
                penalty_parameters_increase_factor=5, bounds_reduction_factor=0.95, penalty_parameters_max=1e8, bounds_min=0.05)),
        forward_model_settings=fm.ConstellarationSettings(vmec_preset_settings=vs.VmecPresetSettings(fidelity="very_low_fidelity")))
    seed_util.seed_everything(123)
    b = srf.SurfaceRZFourier(**json.load(open(sys.argv[3]))["boundary"])
    json.dump(json.loads(b.model_dump_json()), open(os.path.join(out, "seed.json"), "w"))
    t = time.time(); runner.run(b, SET, problems.MHDStableQIStellarator(), 10.0); print("wall", time.time()-t)


if __name__ == "__main__":
    main()
