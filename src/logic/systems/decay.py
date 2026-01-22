"""Exponential decay system: dx/dt = -lambda * x"""

import numpy as np
import sympy as sp
from numpy.typing import NDArray

from src.logic.lean_bridge.symbolic import SymbolicMixin

class DecaySystem(SymbolicMixin):
    r"""
    Exponential decay system with first-order linear ODE.

    The equation is: 
    $$ \frac{dx}{dt} = -\lambda x $$

    Analytic solution: $$ x(t) = x_0 e^{-\lambda t} $$

    Attributes
    ----------
    lambda_ : float, optional
        Decay rate constant, defaults to 1.0

    Notes
    -----
    This system validates the Python-Lean bridge (Phase 2B/2C).
    Matches parametric Picard-Lindelöf proof in lean/ForgeLogic/Decay.lean (decay_picard_parametric theorem for arbitrary initial conditions and intervals).
    First concrete system for vertical integration (Decay -> Lorenz -> Pendulum).

    """

    # CLASS ATTRIBUTE: Define state variable names
    _state_var_names = ["x"]

    def __init__(self, lambda_: float = 1.0) -> None:
        """
        Initialize decay system.

        Parameters
        ----------
        lambda_ : float, optional
            Decay rate constant. Defaults to 1.0
        """

        self.lambda_ = lambda_

    def f(self, t: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
        """
        Compute derivative for decay system.

        Parameters
        ----------
        t : float
            Current time (unused, system is autonomous).
        y : NDArray[np.float64]
            State vector [x].

        Returns
        -------
        NDArray[np.float64]
            The derivative [dx/dt].
        """

        x_val, = y

        dx_dt = -self.lambda_ * x_val

        return np.array([dx_dt])

    def _build_symbolic_equations(self) -> dict[str, sp.Expr]:
        """
        Build symbolic equation for decay system.

        Returns
        -------
        dict[str, sp.Expr]
            Symbolic derivative: {'x': -lambda * x}
        """

        # Create symbolic variable
        x = sp.symbols('x')

        # Build symbolic expressions matching f() equations
        return {"x": -self.lambda_ * x}

