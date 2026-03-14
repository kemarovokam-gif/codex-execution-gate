# CODEX Execution Gate

Minimal execution-bound invariant enforcement harness with tamper-evident audit ledger and replay verification.

## Quickstart (30 seconds)

Clone the repo and run the enforcement harness:

```bash
git clone https://github.com/kemarovokam-gif/codex-execution-gate
cd codex-execution-gate
python quickstart.py
# CODEX Execution-Bound Governance Harness (Public-Safe)

**License:** Proprietary / All Rights Reserved  
**Author:** Kemar Armando Morrison, MBUT Architect

## What this repo demonstrates

**Core principle:** **Proposal ≠ Permission.**

This repository is a **public-safe harness** that demonstrates an **execution-time governance boundary** between any proposal engine and state commitment.

It proves (via runnable code + tests + CI):

- ✅ **Execution-time admissibility gate** (ACCEPT / REJECT / PROJECT)
- ✅ **Projection/repair** for inadmissible proposals (bounded correction)
- ✅ **Hash-chained audit ledger** (tamper-evident)
- ✅ **Deterministic replay verification** (same seed ⇒ same hashes)
- ✅ **CI-enforced tests** (PyTest)

> Note: This is **not** the full proprietary CODEX stack. It is a minimal, public-safe demonstration of enforcement mechanics.

---

## Quickstart (local)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python examples/quickstart.py
pytest -q
```

### Expected output (example)
- Violations handled: 500/500 (100%)
- Committed violations: 0
- Replay verification: PASS
- Tamper detection: PASS

---

## Design summary

- A **proposal engine** emits `z_prop` (a vector state).
- The **gate** evaluates admissibility and chooses:
  - **ACCEPT**: commit as-is
  - **PROJECT**: repair/clip/project into admissible region, then commit
  - **REJECT**: refuse commit (optional path included; demo defaults to PROJECT for repairability)
- Every step is written to a **hash-chained ledger**:
  - `h_t = SHA256(h_{t-1} || canonical_row_t)`

---

## Repo layout

```
codex_gate/        core library
examples/          one-command demo
tests/             enforcement + replay + tamper tests
.github/workflows/ CI pipeline
```

---

## Contact

Kemar Armando Morrison  
kemar.morrison@ou.ac.uk
"""
Minimal Teleken-VÖLUNDR Prototype
----------------------------------
Demonstrates plug-and-play governance flow
without exposing proprietary core engines.
"""

import numpy as np

# --- Minimal Identity Functional ---
class IdentityFunctional:
    def __init__(self, epsilon=0.5):
        self.epsilon = epsilon
        self._I_prev = None

    def compute(self, psi):
        return float(np.sum(np.abs(psi)**2) / max(len(psi), 1))

    def drift(self, psi):
        I = self.compute(psi)
        if self._I_prev is None:
            self._I_prev = I
            return 0.0, True
        dI = abs(I - self._I_prev)
        self._I_prev = I
        return dI, dI <= self.epsilon

# --- Minimal Governance Step ---
def governance_step(state):
    """
    Demonstrates a simple governance check.
    In practice, replace with P23 projection, NIR dissipation, Chimera recurrence.
    """
    identity = IdentityFunctional()
    drift, stable = identity.drift(state)
    status = "OK" if stable else "DRIFT"
    # Example governance: simple normalization
    new_state = state / (np.linalg.norm(state) + 1e-8)
    return new_state, drift, status

# --- Demo Execution ---
if __name__ == "__main__":
    state = np.random.rand(10)
    for step in range(5):
        state, drift, status = governance_step(state)
        print(f"Step {step}: status={status}, drift={drift:.5f}, state={state}")
