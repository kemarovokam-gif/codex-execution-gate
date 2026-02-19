# Reproducibility

This harness is designed to be **deterministic** given:
- a fixed random seed
- a fixed policy configuration (bounds)
- a fixed initial state vector

## What is deterministic?
- The proposal generator sequence
- The gate decisions (based on policy + proposed state)
- The committed states
- The ledger row hashes and the final chain hash

## How to verify determinism
Run:

```bash
python examples/quickstart.py --steps 200 --seed 7
python examples/quickstart.py --steps 200 --seed 7
```

Both runs should output the **same final ledger hash**.

## Tamper evidence
The ledger verifier will fail if any row is modified, removed, or reordered.
