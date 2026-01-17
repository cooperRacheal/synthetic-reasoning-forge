"""Unit tests for ODE system implementations."""

import pytest
import numpy as np
from numpy.testing import assert_allclose

from src.logic.systems.lorenz import LorenzSystem
from src.logic.systems.pendulum import DampedPendulum
from src.logic.systems.blow_up_system import BlowUpSystem


class TestLorenzSystem:
    """Test Lorenz system implementation."""

    def test_derivative_shape(self, lorenz_system, lorenz_ic):
        """Derivative f() returns 3D vector for 3D state."""
        dydt = lorenz_system.f(0.0, lorenz_ic)
        assert dydt.shape == (3,)
        assert dydt.dtype == np.float64

    def test_default_parameters(self):
        """Default parameters match Lorenz 1963 textbook values."""
        sys = LorenzSystem()
        assert sys.sigma == 10.0
        assert sys.rho == 28.0
        assert_allclose(sys.beta, 8/3)

    def test_custom_parameters(self):
        """System accepts custom parameter values."""
        sys = LorenzSystem(sigma=5.0, rho=15.0, beta=2.0)
        assert sys.sigma == 5.0
        assert sys.rho == 15.0
        assert sys.beta == 2.0

class TestDampedPendulum:
    """Test Damped Pendulum system implementation."""

    def test_derivative_shape(self, pendulum_system, pendulum_ic):
        """Derivative f() returns 2D vector for 2D state."""
        dydt = pendulum_system.f(0.0, pendulum_ic)
        assert dydt.shape == (2,)
        assert dydt.dtype == np.float64

    def test_default_parameters(self):
        """Default parameters match Damped Pendulum textbook values."""
        sys = DampedPendulum()
        assert sys.length == 1.0
        assert sys.damping == 0.2
        assert sys.mass == 1.0
        assert sys.gravity == 9.81

    def test_custom_parameters(self):
        """System accepts custom parameter values."""
        sys = DampedPendulum(length=2.0, damping=0.5, mass=2.0, gravity=1.62)
        assert sys.length == 2.0
        assert sys.damping == 0.5
        assert sys.mass == 2.0
        assert sys.gravity == 1.62

