"""Unit tests for PlotterFactory."""

import pytest

from src.logic.plotting.base import ODEPlotter
from src.logic.plotting.factory import PlotterFactory, PlotterNotFoundError
from src.logic.plotting.plotters import ThreeDimensionalPlotter, TwoDimensionalPlotter


class TestPlotterFactory:
    """Test PlotterFactory registry and creation."""

    def test_default_registry_contains_2d_3d(self):
        """Default registry contains 2D and 3D plotters."""

        # Test 2 and 3 exist in registry and correspond to correct Plotter
        assert 2 in PlotterFactory._registry
        assert PlotterFactory._registry[2] == TwoDimensionalPlotter
        assert 3 in PlotterFactory._registry
        assert PlotterFactory._registry[3] == ThreeDimensionalPlotter

        # Test Factory create correct instance of Plotter
        plotter2 = PlotterFactory.create(2)
        assert isinstance(plotter2, TwoDimensionalPlotter)
        plotter3 = PlotterFactory.create(3)
        assert isinstance(plotter3, ThreeDimensionalPlotter)

    def test_create_invalid_dimension_raises_error(self):
        """create() raises PlotterNotFoundError for unregistered dimension."""
        with pytest.raises(PlotterNotFoundError):
            PlotterFactory.create(4)

    def test_register_custom_plotter(self):
        """Verify PlotterFactory.registry() adds a new plotter to registry."""

        # Define test plotter
        class TestPlotter(ODEPlotter):
            def plot(self, t, y, labels=None, title=None, save_path=None):
                pass

        # Register test plotter, create it and verify
        PlotterFactory.register(4, TestPlotter)
        assert PlotterFactory._registry[4] == TestPlotter

        plotter = PlotterFactory.create(4)
        assert isinstance(plotter, TestPlotter)
        assert isinstance(plotter, ODEPlotter)

        # Cleanup
        del PlotterFactory._registry[4]

    def test_register_overwrites_existing_dimension(self):
        """Registering for existing dimension replaces old plotter."""

        # Save original 2D registry object
        original = PlotterFactory._registry[2]

        class New2DPlotter(ODEPlotter):
            def plot(self, t, y, labels=None, title=None, save_path=None):
                pass

        # Overwrite existing 2D plotter in registry
        PlotterFactory.register(2, New2DPlotter)

        # Verify replacement in registry
        assert PlotterFactory._registry[2] == New2DPlotter
        assert PlotterFactory._registry[2] != TwoDimensionalPlotter

        # Restore original 2D registry object
        PlotterFactory._registry[2] = original
