"""Protocol definitions for Synthetic Reasoning Forge."""

from typing import Protocol

import numpy as np
from numpy.typing import NDArray


class ODESystem(Protocol):
    """Protocol for ODE systems compatible with the solver."""

    def f(self, t: float, y: NDArray[np.float64]) -> NDArray[np.float64]: ...
