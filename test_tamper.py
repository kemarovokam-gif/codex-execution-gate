from __future__ import annotations
import random
import copy

from codex_gate.policies import BoxPolicy
from codex_gate.gate import commit_time_gate
from codex_gate.ledger import HashChainedLedger

def propose(prev, rng: random.Random):
    return [v + rng.uniform(-1.5, 1.5) for v in prev]

def test_tamper_detected():
    policy = BoxPolicy(lower=[-2.0]*9, upper=[2.0]*9, max_step_l2=1.2)
    rng = random.Random(9)
    z = [0.0]*9
    ledger = HashChainedLedger()
    for t in range(50):
        z_prop = propose(z, rng)
        d = commit_time_gate(z, z_prop, policy, prefer_project=True)
        ledger.append(t=t, z_prev=z, z_prop=z_prop, decision=d.decision, z_commit=d.z_commit, violations=d.violations)
        z = d.z_commit if d.z_commit is not None else z

    led = ledger.to_json()
    assert HashChainedLedger.verify(led)

    tampered = copy.deepcopy(led)
    tampered["rows"][10]["z_prop"][0] += 0.123  # change a payload value
    assert not HashChainedLedger.verify(tampered)
