"""Custom exceptions for Synthetic Reasoning Forge.

Exceptions provide domain-specific error handling for ODE solvers,
Lean integration, and numerical analysis failures.
"""


class ForgeError(Exception):
    """Base exception for all Forge errors."""


class SolverConvergenceError(ForgeError):
    """ODE solver failed to converge within specified tolerances.

    This typically occurs when:
    - System is stiff and requires implicit solver (LSODA, Radau)
    - Integration step size becomes too small
    - Solution exhibits finite-time blow-up
    """


class LeanTimeoutError(ForgeError):
    """Lean subprocess exceeded time limit.

    Used in Phase 2 when Lean kernel takes too long to verify a proof.
    """


class LeanVerificationError(ForgeError):
    """Lean proof failed to verify.

    Used in Phase 2 when Lean compiler rejects a proof attempt.
    """
