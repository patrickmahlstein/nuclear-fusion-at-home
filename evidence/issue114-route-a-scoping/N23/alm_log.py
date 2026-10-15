"""Picklable wrapper: log every ALM evaluation (objective, constraints, boundary) per worker pid."""
import json, os
import constellaration.optimization.augmented_lagrangian_runner as runner
ORIG = runner.objective_constraints
def objective_constraints_logged(x, scale, problem, unravel, settings, arub):
    (obj, cons), metrics = ORIG(x, scale, problem, unravel, settings, arub)
    rec = dict(objective=float(obj), constraints=[float(c) for c in cons])
    if metrics is not None:
        rec["metrics"] = json.loads(metrics.model_dump_json())
        rec["boundary"] = json.loads(unravel(x*scale).model_dump_json())
    with open(os.path.join(os.environ["N23_LOG"], f"evals-{os.getpid()}.jsonl"), "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    return (obj, cons), metrics
