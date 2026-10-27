"""Run every frozen cell and save all estimates, paired differences and audits."""
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from manufacturing_genius.study import POLICIES, STREAMS, exact_accuracy, simulate_cell, summarize


def run():
    config_bytes = (ROOT / "data/study_config.json").read_bytes()
    config = json.loads(config_bytes)
    assert config['stream_ids'] == STREAMS and config['policies'] == list(POLICIES)
    cells = []
    for i, (delta, a, rho) in enumerate(product(config["delta"], config["risk_size"], config["correlation"])):
        sim = simulate_cell(delta, a, rho, n=config["replicates"], seed=config["master_seed"], scenario=i,
                            sigma_0=config["sigma_0"], sigma_H=config["sigma_H"])
        policies = {p: {k: summarize(v, binary=k == "accuracy") for k, v in metrics.items()}
                    for p, metrics in sim["outcomes"].items()}
        paired = {}
        for p, q in config["paired_comparisons"]:
            paired[p + "-" + q] = {k: summarize(v - sim["outcomes"][q][k])
                                    for k, v in sim["outcomes"][p].items()}
        exact = exact_accuracy(delta, a, rho, config["sigma_0"])
        for p, expected in exact.items():
            if expected is not None:
                s = policies[p]["accuracy"]
                if abs(s["mean"] - expected) > 5 * s["mc_se"] + 1e-12:
                    raise AssertionError(f"MC accuracy disagrees with exact calculation: {i}, {p}")
        if delta:
            for p, metrics in policies.items():
                if abs(metrics["selected_ability"]["mean"] - delta * (metrics["accuracy"]["mean"] - .5)) > 1e-12:
                    raise AssertionError("selected-ability identity failed")
            if exact["equilibrium"] > exact["safe"] + 1e-12:
                raise AssertionError("safe-benchmark inequality failed")
        cells.append({"id": i, "delta": delta, "risk_size": a, "correlation": rho,
                      "policies": policies, "paired": paired, "exact_accuracy": exact,
                      "equilibrium_audit": sim["audit"],
                      "fresh_first_noise_correlation": sim["fresh_first_noise_correlation"]})
    code_paths = ('src/manufacturing_genius/duel.py', 'src/manufacturing_genius/study.py', 'scripts/run_study.py')
    result = {"kind": "new_synthetic_study", "config_sha256": sha256(config_bytes).hexdigest(),
              "code_sha256": {p: sha256((ROOT/p).read_bytes()).hexdigest() for p in code_paths},
              "config": config, "cells": cells}
    dest = ROOT / "data/generated/study.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(f"Saved {len(cells)} cells, {config['replicates']} replicates each: {dest.relative_to(ROOT)}")
    print(f"Maximum unilateral-deviation gain: {max(a['max_deviation_gain'] for c in cells for a in c['equilibrium_audit']):.3g}")


if __name__ == "__main__":
    run()
