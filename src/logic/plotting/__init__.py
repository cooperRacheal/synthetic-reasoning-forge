"""Phase portrait plotting utilities for ODE systems.

This module provides extensible visualization for dynamical systems using
the Strategy pattern. New visualization types can be added by implementing
the PhasePortraitPlotter interface and registering with PlotterFactory.

Architecture
------------
- Strategy Pattern: PhasePortraitPlotter ABC defines interface
- Factory Pattern: PlotterFactory selects plotter based on dimensionality
- Open/Closed: Add plotters based on dimension without modifying existing code

Public API
----------
plot_phase_portrait : function
    Main entry point - automatically selects appropriate plotter
PlotConfig : dataclass
    Configuration for plot styling
PlotterFactory : class
    For advanced usage - register custom plotters
PlotterNotFoundError: exception
    Raised when no plotter exists for dimensionality
PhasePortraitPlotter: ABC
    Base class for implementing custom plotters


Examples 
--------
Basic usage with solver integration: 

>>> from src.logic.solver import solve_ode
>>> from src.logic.systems.lorenz import LorenzSystem
>>> from src.logic.plotting import plot_phase_portrait, PlotConfig
>>>
>>> system = LorenzSystem()
>>> sol = solve_ode(system, (0, 50), [1.0, 0.0, 0.0])
>>>
>>> config = PlotConfig(figsize=(12, 10), dpi=150)
>>> fig = plot_phase_portrait(
...     sol.t, sol.y,
...     labels=['x', 'y', 'z'],
...     title='Lorenz Attractor',
...     config=config,
...     save_path='lorenz.png'
... )

Register custom plotter: 

>>> class MyCustomPlotter(PhasePortraitPlotter):
...     def plot(self, t, y, **kwargs):
...         #Custom visualization logic
...         pass
>>> PlotterFactory.register(4, MyCustomPlotter)
...     #If a 4D plotter
"""

from typing import Optional
import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt

from src.logic.plotting.base import PhasePortraitPlotter
from src.logic.plotting.config import PlotConfig
from src.logic.plotting.factory import PlotterFactory, PlotterNotFoundError
from src.logic.plotting.plotters import TwoDimensionalPlotter, ThreeDimensionalPlotter

def plot_phase_portrait(
    t: NDArray[np.float64],
    y: NDArray[np.float64],
    labels: Optional[list[str]] = None,
    title: Optional[str] = None,
    config: Optional[PlotConfig] = None,
    save_path: Optional[str] = None,
) -> plt.Figure:
    """Plot phase portrait for ODE solution.

    Automatically selects appropriate plotter based on state dimensionality.
    Supports 2D and 3D systems. For higher dimensions, use projection techniques
    or register custom plotters.

    This is the main entry point for the plotting API. Users should call this
    function rather than instantiating plotter directly.

    Parameters
    ----------
    t : NDArray[np.float64]
        Time points from ODE solver, shape (n_points,)
    y : NDArray[np.float64]
        State trajectories, shape (n_states, n_points)
    labels : Optional[list[str]]
        Axis labels for each state dimension, if provided
    title : Optional[str]
        Plot title, if provided
    config : Optional[PlotConfig]   
        Plot configuration (figsize, dpi, style, etc.)
    save_path : Optional[str]
        If provided, save figure to this path

    Returns
    -------
    plt.Figure
        Matplotlib figure object

    Raises
    ------
    PlotterNotFoundError
        If no plotter exists for given dimensionality

    Examples
    --------
    2D (damped pendulum):

    >>> from src.logic.systems.pendulum import DampedPendulum
    >>> pendulum = DampedPendulum()
    >>> sol = solve_ode(pendulum, (0, 20), [np.pi/4, 0.0])
    >>> plot_phase_portrait(sol.t, sol.y, labels=['theta', 'omega'], title='Pendulum')

    3D (Lorenz attractor):

    >>> from src.logic.systems.lorenz import LorenzSystem
    >>> lorenz = LorenzSystem()
    >>> sol = solve_ode(lorenz, (0, 50), [1.0, 0.0, 0.0])
    >>> plot_phase_portrait(sol.t, sol.y, labels=['x', 'y', 'z'], title='Lorenz')

    With custom configuration:

    >>> config = PlotConfig(figsize=(14, 10), dpi=200, line_width=2.0)
    >>> plot_phase_portrait(sol.t, sol.y, config=config, save_path='output.png')
    """

    n_dim = y.shape[0]
    plotter = PlotterFactory.create(n_dim)
    return plotter.plot(
        t, y, labels=labels, title=title, save_path=save_path, config=config
    )

# Public API exports
__all__ = [
    "plot_phase_portrait",
    "PlotConfig",
    "PlotterFactory",
    "PhasePortraitPlotter",
    "PlotterNotFoundError",
]
    




