"""Connection model between two hubs."""

from drone import Drone
from hub import Hub


class Connection:
    """Represent a bidirectional connection between two hubs."""

    def __init__(
        self, origin: Hub, destination: Hub, capacity: int = 1
    ) -> None:
        """Initialize a connection with its maximum transit capacity."""
        self.origin: Hub = origin
        self.destination: Hub = destination
        self.capacity: int = capacity
        self.drones_in_transit: list[Drone] = []

    def is_full(self) -> bool:
        """Return whether the connection has reached its capacity."""
        return len(self.drones_in_transit) >= self.capacity

    def transit_drone(self, drone: Drone) -> None:
        """Add a drone to the connection's in-transit list."""
        self.drones_in_transit.append(drone)

    def clear_drones_in_transit(self) -> None:
        """Remove every in-transit drone from the connection."""
        self.drones_in_transit.clear()
