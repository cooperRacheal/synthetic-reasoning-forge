"""Concrete plotter implementations for different dimensionalities."""

from typing import Optional
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from src.logic.plotting.base import PhasePortraitPlotter
from src.logic.plotting.config import PlotConfig

class TwoDimensionalPlotter(PhasePortraitPlotter):
    """Plotter for 2D phase portraits (e.g., damped pendulum).

    Creates a 2D phase space plot showing trajectory in state space.
    Useful for systems with two state variables (position/velocity, etc.)
    """

    def plot(
        self,
        t: NDArray[np.float64],
        y: NDArray[np.float64],
        labels: Optional[list[str]] = None,
        title: Optional[str] = None,
        save_path: Optional[str] = None,
        config: Optional[PlotConfig] = None,
    ) -> plt.Figure: 
        """Plot 2D phase portrait.

        Parameters
        ----------
        t : NDArray[np.float64]
            Time points, shape (n_points,)
        y : NDArray[np.float64]
            State values, shape (2, n_points)
        labels : Optional[list[str]]
            Labels for [x-axis, y-axis]
        title : Optional[str]
            Plot title, if provided
        save_path : Optional[str]
            Path to save figure, if provided
        config : Optional[PlotConfig]
            Plot configuration, if provided

        Returns
        -------
        plt.Figure
            Matplotlib figure

        Examples
        --------
        >>> plotter = TwoDimensionalPlotter()
        >>> fig = plotter.plot(t, y, labels=['theta', 'omega'], title='Pendulum')
        """

        if config is None: 
            config = PlotConfig()

        if labels is None: 
            labels = ["State 0", "State 1"]

        # Apply matplotlib style
        with plt.style.context(config.style):
            fig, ax = plt.subplots(figsize=config.figsize, dpi=config.dpi)

            # Plot trajectory in phase space
            color = None if config.color == "auto" else config.color
            ax.plot(y[0, :], y[1, :], linewidth=config.line_width, 
                color=color, alpha=config.alpha)

            # Mark start and end points for trajectory direction
            if config.show_markers: 
                ax.plot(y[0, 0], y[1, 0], 'go', 
                    markersize=config.marker_size, label='Start')
                ax.plot(y[0, -1], y[1, -1], 'ro',
                    markersize=config.marker_size, label='End')

            ax.set_xlabel(labels[0], fontsize=12)
            ax.set_ylabel(labels[1], fontsize=12)
            if title:
            	ax.set_title(title, fontsize=14)
            	
            # Grid and legend
            if config.show_grid:
                ax.grid(True, alpha=0.3)
            if config.show_markers:
                ax.legend()

            # Aspect ratio (important for undistorted phase space)
            ax.set_aspect(config.aspect)

            plt.tight_layout()

            # Save if path provided
            if save_path: 
                fig.savefig(save_path, dpi=config.dpi, format=config.save_format)

        return fig

class ThreeDimensionalPlotter(PhasePortraitPlotter):
    """Plotter for 3D phase portraits (e.g. lorenz).

    Creates a 3D phase space plot showing trajectory in state space.
    Useful for systems with three state variables.
    """

    def plot(
        self,
        t: NDArray[np.float64],
        y: NDArray[np.float64],
        labels: Optional[list[str]] = None,
        title: Optional[str] = None,
        save_path: Optional[str] = None,
        config: Optional[PlotConfig] = None,
    ) -> plt.Figure:
        """Plot 3D phase portrait.
        
        Parameters
        ----------
        t : NDArray[np.float64]
            Time points, shape (n_points,)
        y : NDArray[np.float64]
            State values, shape (3, n_points)
        labels : Optional[list[str]]
            Labels for [x-axis, y-axis, z-axis]
        title : Optional[str]
            Plot title, if provided
        save_path : Optional[str]
            Path to save figure, if provided
        config : Optional[PlotConfig]
            Plot configuration, if provided
        
        Returns
        -------
        plt.Figure
            Matplotlib figure
        
        Examples
        --------
        >>> plotter = ThreeDimensionalPlotter()
        >>> fig = plotter.plot(t, y, labels=['x', 'y', 'z'], title = 'Lorenz')
        """
        
        if config is None:
            config = PlotConfig()
            
        if labels is None: 
            labels = ["State 0", "State 1", "State 2"]
            
        # Apply matplotlib style
        with plt.style.context(config.style):
            fig = plt.figure(figsize=config.figsize, dpi=config.dpi)
            ax = fig.add_subplot(111, projection='3d')
            
            # Plot trajectory in phase space
            color = None if config.color == "auto" else config.color
            ax.plot(y[0,:], y[1, :], y[2, :], linewidth=config.line_width,
                color=color, alpha=config.alpha)

            # Mark start and end points for trajectory direction
            if config.show_markers:
                ax.plot([y[0, 0]], [y[1, 0]], [y[2, 0]], 'go',
                    markersize=config.marker_size, label='Start')
                ax.plot([y[0, -1]], [y[1, -1]], [y[2, -1]], 'ro',
                    markersize=config.marker_size, label='End')

            ax.set_xlabel(labels[0], fontsize=12)
            ax.set_ylabel(labels[1], fontsize=12)
            ax.set_zlabel(labels[2], fontsize=12)
            if title:
                ax.set_title(title, fontsize=14)

            # Grid and legend
            if config.show_grid:
                ax.grid(True, alpha=0.3)
            if config.show_markers: 
                ax.legend()

            plt.tight_layout()

            # Save if path provided
            if save_path:
                fig.savefig(save_path, dpi=config.dpi, format=config.save_format)

            return fig

            
