"""Unit tests for concrete plotter implementations."""

import matplotlib.pyplot as plt

from src.logic.plotting.plotters import OneDimensionalPlotter, ThreeDimensionalPlotter, TwoDimensionalPlotter


class TestOneDimensionalPlotter:
    """Test 1D time-series plotter."""

    def test_returns_figure(self, synthetic_1d_trajectory):
        """1D plotter returns matplotlib Figure object."""
        t, y = synthetic_1d_trajectory

        plotter = OneDimensionalPlotter()
        fig = plotter.plot(t, y)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_saves_file(self, synthetic_1d_trajectory, tmp_path):
        """1D plotter saves figure to file when save_path provided."""

        t, y = synthetic_1d_trajectory
        save_path = tmp_path / "test_1d.png"

        plotter = OneDimensionalPlotter()
        fig = plotter.plot(t, y, save_path=str(save_path))

        assert save_path.exists()
        plt.close(fig)

class TestTwoDimensionalPlotter:
    """Test 2D phase portrait plotter."""

    def test_returns_figure(self, synthetic_2d_trajectory):
        """2D plotter returns matplotlib Figure object with minimal object passed in."""
        t, y = synthetic_2d_trajectory

        plotter = TwoDimensionalPlotter()
        fig = plotter.plot(t, y)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_saves_file(self, synthetic_2d_trajectory, tmp_path):
        """2D plotter saves figure to file when save_path provided."""

        t, y = synthetic_2d_trajectory
        save_path = tmp_path / "test_2d.png"

        plotter = TwoDimensionalPlotter()
        fig = plotter.plot(t, y, save_path=str(save_path))

        assert save_path.exists()
        plt.close(fig)


class TestThreeDimensionalPlotter:
    """Test 3D phase portrait plotter."""

    def test_returns_figure(self, synthetic_3d_trajectory):
        """3D plotter returns matplotlib Figure object."""
        t, y = synthetic_3d_trajectory

        plotter = ThreeDimensionalPlotter()
        fig = plotter.plot(t, y)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_saves_file(self, synthetic_3d_trajectory, tmp_path):
        """3D plotter saves figure to file when save_path provided."""

        t, y = synthetic_3d_trajectory
        save_path = tmp_path / "test_3d.png"

        plotter = ThreeDimensionalPlotter()
        fig = plotter.plot(t, y, save_path=str(save_path))

        assert save_path.exists()
        plt.close(fig)
