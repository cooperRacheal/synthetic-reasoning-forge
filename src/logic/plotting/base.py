"""Abstract base class for phase portrait plotters."""

from abc import ABC, abstractmethod
from typing import Optional
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

class PhasePortraitPlotter(ABC):
    """Abstract base class for plotting phase portraits of ODE systems.

    This enforces a consistent interface across all visualization types
    enabling the Factory pattern to work seamlessly.
    """

    @abstractmethod
    def plot(
        self,
        t: NDArray[np.float64],
        y: NDArray[np.float64],
        labels: Optional[list[str]] = None,
        title: Optional[str] = None,
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """Plot phase portrait for ODE solution.

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
