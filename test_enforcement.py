from __future__ import annotations
import random

from codex_gate.policies import BoxPolicy
from codex_gate.gate import commit_time_gate

def propose(prev, rng: random.Random):
    out = []
    for v in prev:
        if rng.random() < 0.2:
            out.append(v + rng.uniform(-7.0, 7.0))
        else:
            out.append(v + rng.uniform(-0.5, 0.5))
    return out

def test_no_committed_box_violations():
    policy = BoxPolicy(lower=[-2.0]*9, upper=[2.0]*9, max_step_l2=1.2)
    rng = random.Random(123)
    z = [0.0]*9
    for _ in range(600):
        z_prop = propose(z, rng)
        d = commit_time_gate(z, z_prop, policy, prefer_project=True)
        if d.z_commit is not None:
            assert all(-2.0 <= v <= 2.0 for v in d.z_commit)
            z = d.z_commit
        else:
            assert all(-2.0 <= v <= 2.0 for v in z)
