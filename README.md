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
