"""Generic ODE solver wrapper using scipy.integrate.solve_ivp.

This module provides solve_ode(), a typed wrapper around scipy's solve_ivp
that works with any ODESystem protocol implementation.
"""

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import OdeSolution, solve_ivp

from src.logic.exceptions import SolverConvergenceError
from src.logic.logger import get_logger
from src.logic.protocols import ODESystem


def solve_ode(
    system: ODESystem, t_span: tuple[float, float], y0: NDArray[np.float64]
) -> OdeSolution:
    """Solve an ODE system over a time interval.

    Wraps scipy.integrate.solve_ivp with logging and error handling.
    Uses default RK45 method with adaptive stepping.

    Parameters
    ----------
    system : ODESystem
        Any object implementing f(t, y) -> dy/dt.
    t_span : tuple[float, float]
        Time interval (t0, tf) for integration.
    y0 : NDArray[np.float64]
        Initial state vector at t0.

    Returns
    -------
    OdeSolution
        Scipy solution object with .t, .y, .success attributes.

    Raises
    ------
    SolverConvergenceError
        If solver fails to converge or encounters numerical issues.
    """
    logger = get_logger(__name__)
    logger.info("Solving an ODE system.")

    ivp_solution = solve_ivp(system.f, t_span, y0)
    if not ivp_solution.success:
        raise SolverConvergenceError(f"ODE solver failed: {ivp_solution.message}")
    logger.info("Success")

    return ivp_solution
