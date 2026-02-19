from __future__ import annotations
from typing import List
import math

def clip_box(z: List[float], lower: List[float], upper: List[float]) -> List[float]:
    return [max(l, min(u, v)) for v, l, u in zip(z, lower, upper)]

def l2_norm(v: List[float]) -> float:
    return math.sqrt(sum(x*x for x in v))

def project_step(prev: List[float], z_prop: List[float], max_step_l2: float) -> List[float]:
    """Rate-limit the step size in L2 (public-safe ULTRA-like clamp)."""
    step = [a - b for a, b in zip(z_prop, prev)]
    n = l2_norm(step)
    if n <= max_step_l2:
        return z_prop
    scale = max_step_l2 / (n + 1e-12)
    return [p + scale*s for p, s in zip(prev, step)]
