"""N24 wrapper: |iota| in the runner's iota constraint (matches the problem's scoring), plus per-eval logging."""
import json, os
import jax.numpy as jnp
import constellaration.optimization.augmented_lagrangian_runner as runner
ORIG = runner.objective_constraints
def objective_constraints_logged(x, scale, problem, unravel, settings, arub):
    (obj, cons), metrics = ORIG(x, scale, problem, unravel, settings, arub)
    rec = dict(objective=float(obj))
    if metrics is not None:
        iota = metrics.edge_rotational_transform_over_n_field_periods
        cons = cons.at[1].set(problem._edge_rotational_transform_over_n_field_periods_lower_bound - abs(iota))
        rec["metrics"] = json.loads(metrics.model_dump_json())
        rec["boundary"] = json.loads(unravel(x*scale).model_dump_json())
    rec["constraints"] = [float(c) for c in cons]
    with open(os.path.join(os.environ["N23_LOG"], f"evals-{os.getpid()}.jsonl"), "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    return (obj, cons), metrics
