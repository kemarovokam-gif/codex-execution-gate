from __future__ import annotations
import argparse
import json
import random
from typing import List

from codex_gate.policies import BoxPolicy
from codex_gate.gate import commit_time_gate
from codex_gate.ledger import HashChainedLedger
from codex_gate.replay import verify_replay

def propose(prev: List[float], rng: random.Random) -> List[float]:
    out = []
    for v in prev:
        if rng.random() < 0.15:
            out.append(v + rng.uniform(-6.0, 6.0))  # likely violate bounds
        else:
            out.append(v + rng.uniform(-0.8, 0.8))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=500)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", type=str, default="")
    args = ap.parse_args()

    policy = BoxPolicy(lower=[-2.0]*9, upper=[2.0]*9, max_step_l2=1.2)
    policy.validate()

    rng = random.Random(args.seed)
    z = [0.0]*9

    ledger = HashChainedLedger()
    violations_total = 0
    committed_violations = 0

    for t in range(args.steps):
        z_prop = propose(z, rng)
        d = commit_time_gate(z, z_prop, policy, prefer_project=True)

        if d.decision in ("PROJECT", "REJECT"):
            violations_total += 1

        z_commit = z if d.z_commit is None else d.z_commit

        if any(v < -2.0 or v > 2.0 for v in z_commit):
            committed_violations += 1

        ledger.append(t=t, z_prev=z, z_prop=z_prop, decision=d.decision, z_commit=d.z_commit, violations=d.violations)
        z = z_commit

    led = ledger.to_json()
    ok = verify_replay(led)

    print(f"Violations handled: {violations_total}/{args.steps} ({(violations_total/args.steps)*100:.1f}%)")
    print(f"Committed violations: {committed_violations}")
    print(f"Replay verification: {'PASS' if ok else 'FAIL'}")
    print(f"Final ledger hash: {led['final_hash']}")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(led, f, indent=2, sort_keys=True)

if __name__ == "__main__":
    main()
