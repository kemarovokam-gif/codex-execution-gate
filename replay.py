from __future__ import annotations
from typing import Any, Dict
from .ledger import HashChainedLedger

def verify_replay(ledger_json: Dict[str, Any]) -> bool:
    return HashChainedLedger.verify(ledger_json)
