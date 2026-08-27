"""Hub model used as a graph node."""

from drone import Drone


class Hub:
    """Represent a graph zone with capacity and drone reservations."""

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: str = "normal",
        color: str | None = None,
        capacity: int = 1,
    ) -> None:
        """Initialize a hub without drones, connections, or reservations."""
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.zone_type: str = zone_type
        self.color: str | None = color
        self.capacity: int = capacity
        self.drones: list[Drone] = []
        self.reservations: list[tuple[Drone, "Hub"]] = []

    def create_reservation(self, drone: Drone, origin_hub: "Hub") -> None:
        """Reserve capacity for a drone and record its origin hub."""
        self.reservations.append((drone, origin_hub))

    def remove_reservation(self, drone: Drone, origin_hub: "Hub") -> None:
        """Remove a drone reservation from this hub."""
        self.reservations.remove((drone, origin_hub))

    def enter_drone(self, drone: Drone) -> None:
        """Add a drone to this hub."""
        self.drones.append(drone)

    def leave_drone(self, drone: Drone) -> None:
        """Remove a drone from this hub."""
        self.drones.remove(drone)

    def get_cost(self) -> int:
        """Return the cost of entering this hub."""
        if self.zone_type == "restricted":
            return 2
        return 1

    def is_full(self) -> bool:
        """Return whether the hub has reached its capacity."""
        occupancy = len(self.drones) + len(self.reservations)
        return occupancy >= self.capacity
