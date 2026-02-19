from __future__ import annotations
import random

from codex_gate.policies import BoxPolicy
from codex_gate.gate import commit_time_gate
from codex_gate.ledger import HashChainedLedger
from codex_gate.replay import verify_replay

def propose(prev, rng: random.Random):
    out = []
    for v in prev:
        if rng.random() < 0.15:
            out.append(v + rng.uniform(-6.0, 6.0))
        else:
            out.append(v + rng.uniform(-0.8, 0.8))
    return out

def run(seed: int):
    policy = BoxPolicy(lower=[-2.0]*9, upper=[2.0]*9, max_step_l2=1.2)
    rng = random.Random(seed)
    z = [0.0]*9
    ledger = HashChainedLedger()
    for t in range(250):
        z_prop = propose(z, rng)
        d = commit_time_gate(z, z_prop, policy, prefer_project=True)
        ledger.append(t=t, z_prev=z, z_prop=z_prop, decision=d.decision, z_commit=d.z_commit, violations=d.violations)
        z = d.z_commit if d.z_commit is not None else z
    return ledger.to_json()

def test_deterministic_final_hash_and_verification():
    a = run(7)
    b = run(7)
    assert a["final_hash"] == b["final_hash"]
    assert verify_replay(a)
    assert verify_replay(b)
