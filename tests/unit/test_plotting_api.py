"""Unit tests for plot_phase_portrait API function."""

import matplotlib.pyplot as plt
import numpy as np
import pytest

from src.logic.plotting import PlotterNotFoundError, plot_phase_portrait


class TestPlotPhasePortrait:
    """Test public API function for phase portrait plotting."""

    def test_2d_dispatch(self, synthetic_2d_trajectory):
        """plot_phase_portrait handles 2D data."""
        t, y = synthetic_2d_trajectory

        fig = plot_phase_portrait(t, y)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_3d_dispatch(self, synthetic_3d_trajectory):
        """plot_phase_portrait handles 3D data."""
        t, y = synthetic_3d_trajectory

        fig = plot_phase_portrait(t, y)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_invalid_dimension_raises_error(self):
        """plot_phase_portrait raises error for unsupported dimension."""
        t = np.linspace(0, 10, 100)
        y = np.random.rand(4, 100)

        with pytest.raises(PlotterNotFoundError):
            plot_phase_portrait(t, y)
