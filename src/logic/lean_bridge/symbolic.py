"""Mixin providing symbolic equation capabilities for ODE systems."""

from typing import Protocol

import sympy as sp


class SymbolicMixin:
    """
    Mixin adding symbolic equation extraction to ODE systems.

    Classes inheriting this mixin must:
    1. Define _state_var_names class attributes (list of variable names)
    2. Implement _build_symbolic_equations() method

    Provides lazy symbolic generation with automatic caching.
    """

    def get_symbolic_equations(self) -> dict[str, sp.Expr]:
        """
        Return symbolic equations as dict mapping variable names to expressions.

        Lazy evaluation: equations built on first call, cached for subsequent calls.

        Returns
        -------
        dict[str, sp.Expr]
            Mapping of state variable names to symbolic derivative expressions.
            Example: {'x': sigma*(y-x), 'y': x*(rho - z) -y, ...}

        Examples
        --------
        >>> lorenz = LorenzSystem(sigma=10, rho=28, beta=8/3)
        >>> eqs = lorenz.get_symbolic_equations()
        >>> eqs['x']
        10*(y - x)
        """

        if not hasattr(self, "_symbolic_cache"):
            self._symbolic_cache = self._build_symbolic_equations()

        return self._symbolic_cache

    def get_state_variables(self) -> list[str]:
        """
        Return list of state variable names.

        Returns
        -------
        list[str]
            State variable names in order (e.g. ['x', 'y', 'z'])
        """
        return self._state_var_names

    def _build_symbolic_equations(self) -> dict[str, sp.Expr]:
        """
        Build symbolic equations for this system.

        Must be implemented by subclass inheriting SymbolicMixin.

        Returns
        -------
        dict[str, sp.Expr]
            Mapping of variable names to symbolic derivative expressions.

        Raises
        ------
        NotImplementedError
            If subclass does not override this method.
        """
        raise NotImplementedError(
            f"{type(self).__name__} must implement _build_symbolic_equations()"
        )


class SymbolicODESystem(Protocol):
    """Protocol for ODE system with symbolic equation support."""

    def get_symbolic_equations(self) -> dict[str, sp.Expr]: ...
    def get_state_variables(self) -> list[str]: ...
