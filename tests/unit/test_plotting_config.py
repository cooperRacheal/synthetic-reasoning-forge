"""Unit test for PlotConfig dataclass."""

import pytest
from src.logic.plotting.config import PlotConfig

class TestPlotConfig:
    """Test PlotConfig dataclass defaults and customization."""

    def test_default_values(self):
        """PlotConfig has correct default values."""

        # Create default PlotConfig with no parameters
        config = PlotConfig()

        # Assert each attribute equals expected default
        assert config.figsize == (10, 8)
        assert config.dpi == 100
        assert config.style == "seaborn-v0_8-darkgrid"
        assert config.save_format == "png"
        assert config.show_grid == False
        assert config.line_width == 1.5
        assert config.color == "auto"
        assert config.alpha == 1.0
        assert config.marker_size == 8.0
        assert config.show_markers == True
        assert config.aspect == "auto"

    def test_custom_values(self):
        """PlotConfig accepts custom parameter values."""

        # Create custom PlotConfig
        config = PlotConfig(
            figsize=(20, 4),
            dpi=200,
            style="default",
            save_format="jpg",
            line_width=2.0,
            color="red",
            alpha=2.0,
            marker_size=7.0,
            show_markers=False,
            aspect="equal"
        )

        # Assert each attribute equals custom assignment
        assert config.figsize == (20, 4)
        assert config.dpi == 200
        assert config.style == "default"
        assert config.save_format == "jpg"
        assert config.show_grid == False
        assert config.line_width == 2.0
        assert config.color == "red"
        assert config.alpha == 2.0
        assert config.marker_size == 7.0
        assert config.show_markers == False
        assert config.aspect == "equal"        
        
