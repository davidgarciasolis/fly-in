"""Data model for a single drone movement."""

from connection import Connection
from drone import Drone
from hub import Hub


class Movement:
    """Represent a drone movement to a hub or through a connection."""

    def __init__(
        self,
        drone: Drone,
        hub: Hub | None = None,
        connection: Connection | None = None,
    ) -> None:
        """Store the drone, destination hub, and connection for a movement."""
        self._drone: Drone = drone
        self._hub: Hub | None = hub
        self._connection: Connection | None = connection

    def __lt__(self, other: "Movement") -> bool:
        """Order movements by their drone identifiers."""
        identifier = self._drone.get_identifier()
        other_identifier = other.get_drone().get_identifier()
        return identifier < other_identifier

    def get_drone(self) -> Drone:
        """Return the drone performing the movement."""
        return self._drone

    def get_hub(self) -> Hub | None:
        """Return the movement destination hub, if any."""
        return self._hub

    def get_connection(self) -> Connection | None:
        """Return the movement connection, if any."""
        return self._connection
