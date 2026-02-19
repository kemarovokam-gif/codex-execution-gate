from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class BoxPolicy:
    """Public-safe admissibility policy: component-wise bounds + L2 step limit."""
    lower: List[float]
    upper: List[float]
    max_step_l2: float

    def validate(self) -> None:
        if len(self.lower) != len(self.upper):
            raise ValueError("lower/upper must have same length")
        if any(l > u for l, u in zip(self.lower, self.upper)):
            raise ValueError("lower must be <= upper for all components")
        if self.max_step_l2 <= 0:
            raise ValueError("max_step_l2 must be positive")
