from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import hashlib
import json

def _sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

@dataclass
class LedgerRow:
    t: int
    z_prev: List[float]
    z_prop: List[float]
    decision: str
    z_commit: Optional[List[float]]
    violations: Dict[str, Any]
    h_prev: str
    h: str

class HashChainedLedger:
    """Tamper-evident ledger: h_t = SHA256(h_{t-1} || row_t)."""

    def __init__(self, genesis: str = "0"*64):
        self.genesis = genesis
        self.rows: List[LedgerRow] = []

    def append(self, *, t: int, z_prev: List[float], z_prop: List[float], decision: str,
               z_commit: Optional[List[float]], violations: Dict[str, Any]) -> LedgerRow:
        h_prev = self.rows[-1].h if self.rows else self.genesis
        row_payload = {
            "t": t,
            "z_prev": z_prev,
            "z_prop": z_prop,
            "decision": decision,
            "z_commit": z_commit,
            "violations": violations,
        }
        h = _sha256((h_prev + _sha256(canonical_json(row_payload))).encode("utf-8"))
        row = LedgerRow(t=t, z_prev=z_prev, z_prop=z_prop, decision=decision, z_commit=z_commit,
                        violations=violations, h_prev=h_prev, h=h)
        self.rows.append(row)
        return row

    def to_json(self) -> Dict[str, Any]:
        return {
            "genesis": self.genesis,
            "rows": [row.__dict__ for row in self.rows],
            "final_hash": self.rows[-1].h if self.rows else self.genesis
        }

    @staticmethod
    def verify(ledger_json: Dict[str, Any]) -> bool:
        genesis = ledger_json["genesis"]
        rows = ledger_json["rows"]
        h_prev = genesis
        for r in rows:
            row_payload = {
                "t": r["t"],
                "z_prev": r["z_prev"],
                "z_prop": r["z_prop"],
                "decision": r["decision"],
                "z_commit": r["z_commit"],
                "violations": r["violations"],
            }
            expected = _sha256((h_prev + _sha256(canonical_json(row_payload))).encode("utf-8"))
            if expected != r["h"]:
                return False
            if r["h_prev"] != h_prev:
                return False
            h_prev = r["h"]
        return True
