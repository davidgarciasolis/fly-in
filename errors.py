
"""Custom exceptions raised by the application."""


class MapConfigurationError(ValueError):
    """Raised when a map configuration cannot be loaded or validated."""
    pass


class SimulationError(RuntimeError):
    """Raised when the simulation cannot be completed."""
    pass
