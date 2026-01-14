"""
Reasoning Forge Logic Package.

This package contains the Python bridge, heuristics, and ODE solver
for the Synthetic Reasoning Forge project.
"""

__version__ = "0.1.0"


from src.logic.solver import solve_ode

__all__ = ["solve_ode"]
