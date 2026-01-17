"""Implementation of the Damped Pendulum as a system of first-order ODEs"""

import numpy as np
from numpy.typing import NDArray


class DampedPendulum:
    r"""
    This model describes the motion of a pendulum of mass $m$ and length $L$,
    subject to a damping force with coefficient $b$.

    The second order equation is:
    $$
    \frac{d^2\theta}{dt^2} + \frac{b}{m}\frac{d\theta}{dt}
    + \frac{g}{L}\sin{(\theta)} = 0
    $$

    Converted to a first-order system where $\omega = \frac{d\theta}{d t}$:
    $$ \frac{d\theta}{dt} = \omega $$
    $$ \frac{d\omega}{dt} = -\frac{b}{m}\omega - \frac{g}{L}\sin{(\theta)} $$

    Attributes
    ----------
    length : float, optional
        Length of the pendulum arm ($L$) in meters. Defaults to 1.0 m
        (standard meter stick length).
    damping : float, optional
        Damping coefficient ($b$) in N·m·s/rad representing air resistance
        or friction. Defaults to 0.2 (light damping, shows clear spiral).
    mass : float, optional
        Mass of the pendulum bob ($m$) in kilograms. Defaults to 1.0 kg
        (unit mass, simplifies calculations).
    gravity : float, optional
        Acceleration due to gravity ($g$) in m/s². Defaults to 9.81 m/s²
        (Earth gravity).
    """

    def __init__(
        self, length: float = 1.0, damping: float = 0.2, mass: float = 1.0, gravity: float = 9.81
    ) -> None:
        self.length = length
        self.damping = damping
        self.mass = mass
        self.gravity = gravity

    def f(self, t: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
        r"""
        Compute the derivatives of the pendulum state.

        Parameters
        ----------
        t : float
            Current time (the system is autonomous).
        y : NDArray[np.float64]
            State vector containing [angle, angular_velocity].
            - theta (rad): y[0]
            - omega (rad/s): y[1]

        Returns
        -------
        NDArray[np.float64]
            The derivative [d_theta/dt, d_omega/dt].

        Note: The solution shows damped oscillations, where amplitude A decays
        exponentially as $e^{-\left(\frac{b}{2m}\right)t}$.
        """

        theta, omega = y

        dtheta_dt = omega
        domega_dt = -(self.damping / self.mass) * omega - (
            self.gravity / self.length
        ) * np.sin(theta)

        return np.array([dtheta_dt, domega_dt])
