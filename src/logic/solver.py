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
    system: ODESystem, 
    t_span: tuple[float, float], 
    y0: NDArray[np.float64],
    method: str = "RK45",
    auto_fallback: bool = True
) -> OdeSolution:
    """Solve an ODE system over a time interval.

    Wraps scipy.integrate.solve_ivp with logging and error handling.
    Supports multiple integration methods with automatic stiffness handling.

    Parameters
    ----------
    system : ODESystem
        Any object implementing f(t, y) -> dy/dt.
    t_span : tuple[float, float]
        Time interval (t0, tf) for integration.
    y0 : NDArray[np.float64]
        Initial state vector at t0.
    method : str, default "RK45"
        Integration algorithm for solve_ivp. 
        Options:    'RK45' (explicit Runge-Kutta, non-stiff)
                    'LSODA' (adaptive stiffness detection),
                    'Radau' / 'BDF' (implicit, stiff systems)
        See scipy.integrate.solve_ivp documentation.
    auto_fallback : bool, default True
        Enable automatic retry with LSODA if initial method fails convergence.
        Prevents failures on stiff systems. Disable for strict method control.
        (should only be done by advanced users)

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

    ivp_solution = solve_ivp(system.f, t_span, y0, method=method)
    if not ivp_solution.success and auto_fallback and method != "LSODA":
        logger.warning(f"{method} failed ({ivp_solution.message}), retrying with LSODA")
        ivp_solution = solve_ivp(system.f, t_span, y0, method="LSODA")

        if not ivp_solution.success:
            raise SolverConvergenceError(f"Both {method} and LSODA failed: {ivp_solution.message}")

        logger.info("Success with LSODA fallback")

    elif not ivp_solution.success:  
        raise SolverConvergenceError(f"{method} failed: {ivp_solution.message}")

    else:
        logger.info("Success")

    return ivp_solution
