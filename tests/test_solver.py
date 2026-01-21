"""Quick manual test script for ODE solver.

This is a simple smoke test script for rapid development iteration.
For comprehensive unit tests, see tests/unit/test_solver.py.

Usage:
    python tests/test_solver.py

Expected Output:
    - Lorenz system solves successfully
    - Pendulum system solves successfully
    - BlowUpSystem correctly raises SolverConvergenceError
"""

import numpy as np

from src.logic.exceptions import SolverConvergenceError
from src.logic.solver import solve_ode
from src.logic.systems import BlowUpSystem, DampedPendulum, LorenzSystem

# Test Lorenz
print("Testing Lorenz...")
lorenz = LorenzSystem(10, 28, 8 / 3)
sol = solve_ode(lorenz, (0, 1), np.array([1.0, 1.0, 1.0]))
print(f" Success: {sol.success}, Time points: {len(sol.t)}")

# Test Pendulum
print("Testing Pendulum...")
pendulum = DampedPendulum(length=1.0, damping=0.5, mass=1.0)
sol = solve_ode(pendulum, (0, 10), np.array([0.5, 0.0]))
print(f" Success: {sol.success}, Time points: {len(sol.t)}")

# Test triggering solver failure to verify error handling
print("Testing error handling...")
blowUpSystem = BlowUpSystem()
try:
    sol = solve_ode(blowUpSystem, (0, 10), np.array([1.0]))
    print(" ERROR: Should have raised SolverConvergenceError!")
except SolverConvergenceError:
    print(" Success: You blew up the system.")
