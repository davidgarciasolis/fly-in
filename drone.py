
"""Drone model used by the simulator."""


class Drone:
    """Represent a drone with a unique identifier."""

    def __init__(self, identifier: int) -> None:
        """Initialize the drone with its identifier."""
        self.identifier: int = identifier

    def get_identifier(self) -> int:
        """Return the drone's unique identifier."""
        return self.identifier
