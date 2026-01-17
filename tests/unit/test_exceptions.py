"""Unit tests for custom exception hierarchy."""

import pytest

from src.logic.exceptions import (
    ForgeError,
    LeanTimeoutError,
    LeanVerificationError,
    SolverConvergenceError,
)


class TestExceptionHierarchy:
    """Test exception inheritance and basic functionality."""

    def test_forge_error_is_exception(self):
        """ForgeError inherits from base Exception."""
        assert issubclass(ForgeError, Exception)

    def test_all_exceptions_inherit_from_forge_error(self):
        """All custom exceptions inherit from ForgeError base class."""

        assert issubclass(SolverConvergenceError, ForgeError)
        assert issubclass(LeanTimeoutError, ForgeError)
        assert issubclass(LeanVerificationError, ForgeError)

    def test_exceptions_can_be_raised(self):
        """All exception types can be raised."""
        with pytest.raises(SolverConvergenceError):
            raise SolverConvergenceError()
        with pytest.raises(LeanTimeoutError):
            raise LeanTimeoutError()
        with pytest.raises(LeanVerificationError):
            raise LeanVerificationError()
        with pytest.raises(ForgeError):
            raise ForgeError()
