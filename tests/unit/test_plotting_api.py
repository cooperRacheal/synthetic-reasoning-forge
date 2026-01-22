"""Unit tests for plot_ode API function."""

import matplotlib.pyplot as plt
import numpy as np
import pytest

from src.logic.plotting import PlotterNotFoundError, plot_ode


class TestPlotODE:
    """Test public API function for ODE plotting."""

    def test_2d_dispatch(self, synthetic_2d_trajectory):
        """plot_ode handles 2D data."""
        t, y = synthetic_2d_trajectory

        fig = plot_ode(t, y)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_3d_dispatch(self, synthetic_3d_trajectory):
        """plot_ode handles 3D data."""
        t, y = synthetic_3d_trajectory

        fig = plot_ode(t, y)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_invalid_dimension_raises_error(self):
        """plot_ode raises error for unsupported dimension."""
        t = np.linspace(0, 10, 100)
        y = np.random.rand(4, 100)

        with pytest.raises(PlotterNotFoundError):
            plot_ode(t, y)
