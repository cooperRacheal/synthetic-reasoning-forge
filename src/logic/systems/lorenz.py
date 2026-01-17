"""Implementation of the Lorenz system of Ordinary Differential Equations"""

import numpy as np
from numpy.typing import NDArray


class LorenzSystem:
    r"""
    The Lorenz system is a system of three ordinary differential equations
    first studied by Edward Lorenz. It is notable for having chaotic solutions
    for certain parameter values and starting conditions.

    The equations are defined as:
    $$ \frac{dx}{dt} = \sigma(y - x) $$
    $$ \frac{dy}{dt} = x(\rho - z) - y $$
    $$ \frac{dz}{dt} = xy - \beta z $$

    Attributes
    ----------
    sigma : float, optional
        The Prandtl number (dimensionless) representing the ratio of momentum
        diffusivity to thermal diffusivity. Defaults to 10.0 (standard chaotic regime).
    rho : float, optional
        The Rayleigh number (dimensionless) representing the temperature difference
        between the top and bottom of the fluid. Defaults to 28.0 (standard chaotic
        regime).
    beta : float, optional
        A geometric factor (dimensionless) related to the physical dimensions of
        the layer. Defaults to 8/3 ≈ 2.667 (standard chaotic regime).
    """

    def __init__(
        self, sigma: float = 10.0, rho: float = 28.0, beta: float = 8 / 3
    ) -> None:
        self.sigma = sigma
        self.rho = rho
        self.beta = beta

    def f(self, t: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
        """
        Compute the derivatives for the Lorenz system at the current state.

        This method is compatible with 'scipy.integrate.solve_ivp'.

        Parameters
        ----------
        t : float
                Current time. Required by ODE solvers, though the Lorenz
                system is autonomous (not explicitly dependent on time).
        y : NDArray[np.float64]
                The state vector [x, y, z].

        Returns
        -------
        NDArray[np.float64]
                The time derivatives [dx/dt, dy/dt, dz/dt].
        """

        x_val, y_val, z_val = y

        dx_dt = self.sigma * (y_val - x_val)
        dy_dt = x_val * (self.rho - z_val) - y_val
        dz_dt = x_val * y_val - self.beta * z_val

        return np.array([dx_dt, dy_dt, dz_dt])
