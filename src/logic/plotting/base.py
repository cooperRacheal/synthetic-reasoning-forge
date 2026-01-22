"""Abstract base class for ODE solution plotters."""

from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray


class ODEPlotter(ABC):
    """Abstract base class for plotting ODE solution trajectories.

    Supports both phase-space plots (state vs state) and 
    time-domain plots (time vs state). Enforces consistent interface
    across all visualization types for Factory pattern compatibility.
    """

    @abstractmethod
    def plot(
        self,
        t: NDArray[np.float64],
        y: NDArray[np.float64],
        labels: list[str] | None = None,
        title: str | None = None,
        save_path: str | None = None,
    ) -> plt.Figure:
        """Plot ODE solution trajectory.

        Parameters
        ----------
        t : NDArray[np.float64]
            Time points, shape (n_points,)
        y : NDArray[np.float64]
            State values, shape (n_states, n_points)
        labels : Optional[list[str]]
            Axis labels for each dimension, if provided
        title : Optional[str]
            Plot title, if provided
        save_path : Optional[str]
            If provided, save figure to this path

        Returns
        -------
        plt.Figure
            Matplotlib figure object

        Raises
        ------
        TypeError
            If subclass doesn't implement this method
        """
        pass
