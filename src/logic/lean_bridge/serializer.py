"""
JSON serialization for Python-Lean bridge with exact rational
representation.

POC: Serializes DecaySystem to Rat-based JSON for Lean
verification.
Enforces Phase 3A constraints (x0=5, t in [-0.1,0.1], lambda = 1).
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any
from fractions import Fraction

if TYPE_CHECKING:
    from src.logic.systems.decay import DecaySystem

def to_rational(value: float) -> dict[str, int]:
    """Convert float to rational JSON representation."""
    f = Fraction(value).limit_denominator()
    return {"num": f.numerator, "den": f.denominator}

class DecaySerializer: 
    # Phase 3A hardcoded constants
    PHASE_3A_T0 = 0.0
    PHASE_3A_X0 = 5.0
    PHASE_3A_TMIN = -0.1
    PHASE_3A_TMAX = 0.1
    PHASE_3A_LAMBDA = 1.0

    def __init__(self, system: DecaySystem) -> None:
        # Validate lambda matches Phase 3A constraint
        if system.lambda_ != self.PHASE_3A_LAMBDA:
            raise ValueError(
                f"POC requires lambda={self.PHASE_3A_LAMBDA}, "
                f"got {system.lambda_} (Phase 3A constraint)"
            )
        self.system = system

    def to_json(
        self, t0: float, x0: float, tmin: float, tmax: float
    ) -> str: 
        # Validate all parameters match Phase 3A constraints
        if t0 != self.PHASE_3A_T0:
            raise ValueError(f"POC requires t0={self.PHASE_3A_T0}, got {t0}")
        if x0 != self.PHASE_3A_X0:
            raise ValueError(f"POC requires x0={self.PHASE_3A_X0}, got {x0}")
        if tmin != self.PHASE_3A_TMIN:
            raise ValueError(f"POC requires tmin={self.PHASE_3A_TMIN}, got {tmin}")
        if tmax != self.PHASE_3A_TMAX:
            raise ValueError(f"POC requires tmax={self.PHASE_3A_TMAX}, got {tmax}")

        # Build payload with Rat representation
        payload: dict[str, Any] = {
            "system_type": "decay",
            "initial_condition": {
                "t0": to_rational(t0),
                "x0": to_rational(x0),
            },
            "interval": {
                "tmin": to_rational(tmin),
                "tmax": to_rational(tmax),
            },
            "parameters": {
                "lambda": to_rational(self.system.lambda_),
            },
        }

        return json.dumps(payload)
