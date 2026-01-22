"""Factory for creating plotters based on dimensionality."""

from src.logic.exceptions import ForgeError
from src.logic.plotting.base import ODEPlotter
from src.logic.plotting.plotters import OneDimensionalPlotter, ThreeDimensionalPlotter, TwoDimensionalPlotter


class PlotterNotFoundError(ForgeError):
    """Raised when no plotter exists for input dimensionality."""

    pass


class PlotterFactory:
    """Factory for creating phase portrait plotters.

    Uses registry pattern to map dimensionality to plotter classes.
    New plotters can be registered without modifying existing code.

    Examples
    --------
    Basic usage:

    >>> plotter = PlotterFactory.create(3) #Returns ThreeDimensionalPlotter
    >>> fig = plotter.plot(t, y)

    Register custom plotter:

    >>> class BifurcationPlotter(ODEPlotter):
    ... def plot(self, t, y, *kwargs): ...
    >>> PlotterFactory.register("bifurcation", BifurcationPlotter)
    """

    _registry: dict[int, type[ODEPlotter]] = {
        1: OneDimensionalPlotter,
        2: TwoDimensionalPlotter,
        3: ThreeDimensionalPlotter,
    }

    @classmethod
    def create(cls, n_dim: int) -> ODEPlotter:
        """Create plotter for given dimensionality.

        Parameters
        ---------
        n_dim : int
            State space dimensionality

        Returns
        -------
        ODEPlotter
            Concrete plotter instance

        Raises
        ------
        PlotterNotFoundError
            If no plotter registered for dimensionality

        Examples
        --------
        >>> plotter = PlotterFactory.create(2)
        >>> isinstance(plotter, TwoDimensionalPlotter)
        True
        """

        if n_dim not in cls._registry:
            raise PlotterNotFoundError(
                f"No plotter registered for {n_dim}D systems. "
                f"Available dimensions: {list(cls._registry.keys())}"
            )

        plotter_class = cls._registry[n_dim]
        return plotter_class()

    @classmethod
    def register(cls, n_dim: int, plotter_class: type[ODEPlotter]) -> None:
        """Register new plotter for dimensionality.

        Enable extending the factory without modifying this file.

        Parameters
        ----------
        n_dim : int
            Dimensionality this plotter handles
        plotter_class : Type[ODEPlotter]
            Plotter class to register (must inherit from ODEPlotter)

        Examples
        --------
        >>> class CustomPlotter(ODEPlotter):
        ...     def plot(self, t, y, **kwargs): ...
        >>> PlotterFactory.register(4, CustomPlotter)
        """
        cls._registry[n_dim] = plotter_class
