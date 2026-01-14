"""Pathological ODE system for testing solver error handling.

This module provides BlowUpSystem, which has a finite-time singularity
designed to trigger solver convergence failures.
"""

import numpy as np
from numpy.typing import NDArray


class BlowUpSystem:
    """ODE system with finite-time singularity: dy/dt = y^2.

    For positive initial conditions, solution explodes to infinity in finite time,
    forcing the solver to fail. Used to verify SolverConvergenceError handling.
    """

    def f(self, t: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
        """Compute derivative dy/dt = y^2.

        Parameters
        ----------
        t : float
            Time (unused, system is autonomous).
        y : NDArray[np.float64]
            State vector.

        Returns
        -------
        NDArray[np.float64]
            Derivative vector (same shape as y).
        """
        return y**2
