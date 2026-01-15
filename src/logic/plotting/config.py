"""Configuration for phase portrait plotting."""

from dataclasses import dataclass


@dataclass
class PlotConfig:
    """Configuration for plot styling and output.

    Attributes
    ----------
    figsize : tuple[int, int]
        Figure dimensions in inches (width, height)
    dpi : int
        Resolution for saved figures
    style : str
        Matplotlib style name
    save_format : str
        File format for saved figures (png, pdf, etc...)
    show_grid : bool
        Whether to display grid lines
    line_width : float
        Width of plotted trajectory lines
    color : str
        Color of plotted trajectory lines (or 'auto' for default)
    alpha : float
        Line transparency (0.0 transparent to 1.0 opaque)
    marker_size: float
        Size of start/end point markers
    show_markers: bool
        Whether to show the start/end markers
    aspect: str
        Aspect ratio ('auto' or 'equal' for undistorted phase space)
    """

    figsize: tuple[int, int] = (10, 8)
    dpi : int = 100
    style : str = "seaborn-v0_8-darkgrid"
    save_format : str = "png"
    show_grid: bool = False
    line_width: float = 1.5
    color: str = "auto"
    alpha: float = 1.0
    marker_size: float = 8.0
    show_markers: bool = True
    aspect: str = "auto"    




