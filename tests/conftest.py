import numpy as np
import pytest
from numpy.typing import NDArray

from src.logic.systems.blow_up_system import BlowUpSystem
from src.logic.systems.lorenz import LorenzSystem
from src.logic.systems.pendulum import DampedPendulum


@pytest.fixture
def lorenz_system() -> LorenzSystem:
    """Fixture: Lorenz system textbook defaults."""
    return LorenzSystem(sigma=10.0, rho=28.0, beta=8 / 3)


@pytest.fixture
def pendulum_system() -> DampedPendulum:
    """Fixture: Damped pendulum system textbook defaults."""
    return DampedPendulum(length=1.0, damping=0.2, mass=1.0, gravity=9.81)


@pytest.fixture
def blowup_system() -> BlowUpSystem:
    """Fixture: Blow-up system for error handling tests."""
    return BlowUpSystem()


@pytest.fixture
def default_t_span() -> tuple[float, float]:
    """Fixture: Default time span for integration."""
    return (0.0, 10.0)


@pytest.fixture
def lorenz_ic() -> NDArray[np.float64]:
    """Fixture: Initial condition for Lorenz system."""
    return np.array([1.0, 1.0, 1.0])


@pytest.fixture
def pendulum_ic() -> NDArray[np.float64]:
    """Fixture: Initial condition for pendulum (theta = pi/4,
    omega = 0)."""
    return np.array([np.pi / 4, 0.0])


@pytest.fixture
def blowup_ic() -> NDArray[np.float64]:
    """Fixture: Initial conditions for blow-up system."""
    return np.array([1.0])


@pytest.fixture
def synthetic_2d_trajectory() -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Fixture: Synthetic 2D trajectory for plotting tests."""
    t = np.linspace(0, 10, 100)
    y = np.array([np.sin(t), np.cos(t)])  # shape (2, 100)
    return t, y


@pytest.fixture
def synthetic_3d_trajectory() -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Fixture: Synthetic 3D trajectory for plotting tests."""
    t = np.linspace(0, 10, 100)
    y = np.array([np.sin(t), np.cos(t), t / 10])  # shape (3, 100)
    return t, y
