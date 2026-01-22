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

    
