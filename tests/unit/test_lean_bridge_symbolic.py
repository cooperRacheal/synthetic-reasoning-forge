"""Tests for SymbolicMixin and symbolic equation extraction."""

import numpy as np
import pytest
import sympy as sp

from src.logic.lean_bridge.symbolic import SymbolicMixin
from src.logic.systems.lorenz import LorenzSystem


# Test helper classes
class BadSystemNoStateVars(SymbolicMixin):
    """Test helper: Missing _state_var_names."""

    def _build_symbolic_equations(self):
        return {}


class BadSystemNoEquations(SymbolicMixin):
    """Test helper: Missing _build_symbolic_equations override."""

    _state_var_names = ["x"]


@pytest.fixture
def lorenz_default():
    """Default Lorenz system (sigma=10, rho=28, beta=8/3)."""
    return LorenzSystem()


def test_lorenz_has_symbolic_methods(lorenz_default):
    """LorenzSystem should have get_symbolic_equations() and get_state_variables()."""
    assert hasattr(lorenz_default, "get_symbolic_equations")
    assert hasattr(lorenz_default, "get_state_variables")
    assert callable(lorenz_default.get_symbolic_equations)
    assert callable(lorenz_default.get_state_variables)


def test_get_state_variables_returns_correct_names(lorenz_default):
    """get_state_variables() should return ['x', 'y', 'z']."""
    state_vars = lorenz_default.get_state_variables()
    assert state_vars == ["x", "y", "z"]


def test_get_symbolic_equations_returns_dict(lorenz_default):
    """get_symbolic_equations() should return dict with x, y, z keys."""
    eqs = lorenz_default.get_symbolic_equations()
    assert isinstance(eqs, dict)
    assert set(eqs.keys()) == {"x", "y", "z"}
    assert all(isinstance(v, sp.Expr) for v in eqs.values())


def test_symbolic_equations_cached(lorenz_default):
    """Symbolic equations should be built once and cached."""
    eqs1 = lorenz_default.get_symbolic_equations()
    eqs2 = lorenz_default.get_symbolic_equations()

    # Should return same cached dict object
    assert eqs1 is eqs2

    # Cache attribute should exist after first call
    assert hasattr(lorenz_default, "_symbolic_cache")
    assert lorenz_default._symbolic_cache is eqs1


def test_independent_caches_per_instance():
    """Different instances should have independent symbolic caches."""
    lorenz1 = LorenzSystem(sigma=10)
    lorenz2 = LorenzSystem(sigma=15)

    eqs1 = lorenz1.get_symbolic_equations()
    eqs2 = lorenz2.get_symbolic_equations()

    # Different instances should have different cache objects
    assert eqs1 is not eqs2
    assert lorenz1._symbolic_cache is not lorenz2._symbolic_cache


def test_missing_state_var_names_raises_error():
    """Mixin should fail gracefully if _state_var_names not defined."""
    bad = BadSystemNoStateVars()
    with pytest.raises(AttributeError):
        bad.get_state_variables()


def test_missing_build_equations_raises_error():
    """Mixin should raise NotImplementedError if _build_symbolic_equations()
    not overridden.
    """
    bad = BadSystemNoEquations()
    with pytest.raises(NotImplementedError):
        bad.get_symbolic_equations()


def test_symbolic_expressions_contain_parameters(lorenz_default):
    """Symbolic equations should contain parameter values."""
    eqs = lorenz_default.get_symbolic_equations()
    x, y, z = sp.symbols("x y z")

    # dx/dt should be: sigma * (y - x) with sigma=10 for default lorenz
    expected_dx = 10 * (y - x)
    assert eqs["x"].equals(expected_dx)

    # dy/dt should be: x * (rho - z) - y with rho=28 for default lorenz
    expected_dy = x * (28 - z) - y
    assert eqs["y"].equals(expected_dy)

    # dz/dt should be x * y - beta * z with beta=8/3 for default lorenz
    expected_dz = x * y - (8 / 3) * z
    assert eqs["z"].equals(expected_dz)


def test_custom_parameters_embedded_in_equations():
    """Symbolic equations should reflect custom parameter values."""
    custom_lorenz = LorenzSystem(sigma=5, rho=20, beta=1)
    eqs = custom_lorenz.get_symbolic_equations()

    x, y, z = sp.symbols("x y z")

    # Check sigma=5 in dx/dt
    expected_dx = 5 * (y - x)
    assert eqs["x"].equals(expected_dx)

    # Check rho=20 in dy/dt
    expected_dy = x * (20 - z) - y
    assert eqs["y"].equals(expected_dy)

    # Check beta=1 in dz/dt
    expected_dz = x * y - (1) * z
    assert eqs["z"].equals(expected_dz)


def test_symbolic_numerical_correspondence(lorenz_default):
    """Symbolic equations should structurally match numerical f() implementation."""

    # Get symbolic equations
    eqs = lorenz_default.get_symbolic_equations()
    x, y, z = sp.symbols("x y z")

    # Test point
    test_vals = {"x": 1.0, "y": 2.0, "z": 3.0}

    # Evaluate symbolic equations at test point
    symbolic_dx = float(eqs["x"].subs(test_vals))
    symbolic_dy = float(eqs["y"].subs(test_vals))
    symbolic_dz = float(eqs["z"].subs(test_vals))

    # Evaluate numerical f() at same point
    numerical = lorenz_default.f(0, np.array([1.0, 2.0, 3.0]))

    # Check that symbolic and numerical values match
    assert np.isclose(symbolic_dx, numerical[0])
    assert np.isclose(symbolic_dy, numerical[1])
    assert np.isclose(symbolic_dz, numerical[2])
