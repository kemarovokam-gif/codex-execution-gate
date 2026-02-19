from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional

from .policies import BoxPolicy
from .projector import clip_box, project_step, l2_norm

@dataclass
class GateDecision:
    decision: str  # ACCEPT / PROJECT / REJECT
    z_commit: Optional[List[float]]
    violations: Dict[str, object]

def check_box(z: List[float], policy: BoxPolicy) -> Dict[str, object]:
    out = []
    for i, (v, lo, hi) in enumerate(zip(z, policy.lower, policy.upper)):
        if v < lo or v > hi:
            out.append(i)
    return {"box": {"indices": out, "count": len(out)}} if out else {}

def commit_time_gate(z_prev: List[float], z_prop: List[float], policy: BoxPolicy,
                     prefer_project: bool = True) -> GateDecision:
    """Execution-time gate: validate at commit boundary and optionally project into admissible set."""
    v = {}
    v.update(check_box(z_prop, policy))

    step_norm = l2_norm([a - b for a, b in zip(z_prop, z_prev)])
    if step_norm > policy.max_step_l2:
        v["step_l2"] = {"norm": step_norm, "max": policy.max_step_l2}

    if not v:
        return GateDecision(decision="ACCEPT", z_commit=z_prop, violations={})

    if prefer_project:
        z1 = project_step(z_prev, z_prop, policy.max_step_l2)
        z2 = clip_box(z1, policy.lower, policy.upper)

        v_post = {}
        v_post.update(check_box(z2, policy))
        step_norm_post = l2_norm([a - b for a, b in zip(z2, z_prev)])
        if step_norm_post > policy.max_step_l2 + 1e-9:
            v_post["step_l2"] = {"norm": step_norm_post, "max": policy.max_step_l2}

        if v_post:
            return GateDecision(decision="REJECT", z_commit=None, violations={"pre": v, "post": v_post})
        return GateDecision(decision="PROJECT", z_commit=z2, violations={"pre": v, "post": {}})

    return GateDecision(decision="REJECT", z_commit=None, violations=v)
