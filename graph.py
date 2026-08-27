"""Graph model that stores hubs, connections, and drones."""

from connection import Connection
from drone import Drone
from hub import Hub


class Graph:
    """Build and manage the hub graph for a simulation."""

    def __init__(self, configuration: list[str]) -> None:
        """Initialize the graph from validated map configuration lines."""
        self.drone_count: int
        self.start_hub: Hub
        self.end_hub: Hub
        self.hubs: dict[str, Hub] = {}
        self.connections: list[Connection] = []
        self.drones: list[Drone] = []
        self._build(configuration)

    def get_neighbors(self, hub: Hub) -> list[Hub]:
        """Return the hubs directly connected to the given hub."""
        neighbors: list[Hub] = []
        for connection in self.connections:
            if connection.origin == hub:
                neighbors.append(connection.destination)
            elif connection.destination == hub:
                neighbors.append(connection.origin)
        return neighbors

    def get_drone_hub(self, drone: Drone) -> Hub | None:
        """Return the hub currently containing the given drone."""
        for hub in self.hubs.values():
            if drone in hub.drones:
                return hub
        return None

    def get_hubs_with_reservations(self) -> list[Hub]:
        """Return hubs that have active drone reservations."""
        return [hub for hub in self.hubs.values() if hub.reservations]

    def clear_connections(self) -> None:
        """Clear the in-transit drone lists for all connections."""
        for connection in self.connections:
            connection.clear_drones_in_transit()

    def get_connection(self, origin: Hub, destination: Hub) -> Connection:
        """Return the bidirectional connection between two hubs."""
        for connection in self.connections:
            if (
                connection.origin == origin
                and connection.destination == destination
            ):
                return connection
            if (
                connection.origin == destination
                and connection.destination == origin
            ):
                return connection
        raise RuntimeError("Los hubs indicados no tienen una conexión.")

    def _build(self, configuration: list[str]) -> None:
        """Build graph elements and place drones in the start hub."""
        for line in configuration:
            line = line.strip()
            if line.startswith("nb_drones:"):
                drone_count = line.removeprefix("nb_drones:").strip()
                self.drone_count = int(drone_count)
            elif line.startswith("start_hub:"):
                content = line.removeprefix("start_hub:").strip()
                hub = self._create_hub(content)
                hub.capacity = self.drone_count
                self.start_hub = hub
                self.hubs[hub.name] = hub
            elif line.startswith("end_hub:"):
                content = line.removeprefix("end_hub:").strip()
                hub = self._create_hub(content)
                hub.capacity = self.drone_count
                self.end_hub = hub
                self.hubs[hub.name] = hub
            elif line.startswith("hub:"):
                content = line.removeprefix("hub:").strip()
                hub = self._create_hub(content)
                self.hubs[hub.name] = hub
            elif line.startswith("connection:"):
                content = line.removeprefix("connection:").strip()
                self.connections.append(self._create_connection(content))

        for identifier in range(1, self.drone_count + 1):
            drone = Drone(identifier)
            self.drones.append(drone)
            self.start_hub.enter_drone(drone)

    def _create_hub(self, content: str) -> Hub:
        """Create a hub from its map configuration content."""
        data = content.split("[")
        required_parts = data[0].split()
        name = required_parts[0]
        x = int(required_parts[1])
        y = int(required_parts[2])
        zone_type = "normal"
        color = None
        capacity = 1
        if len(data) == 2:
            options = data[1].removesuffix("]").split()
            for option in options:
                key, value = option.split("=")
                if key == "zone":
                    zone_type = value
                elif key == "color":
                    color = value
                elif key == "max_drones":
                    capacity = int(value)
        return Hub(name, x, y, zone_type, color, capacity)

    def _create_connection(self, content: str) -> Connection:
        """Create a connection from its map configuration content."""
        data = content.split("[")
        hub_names = data[0].strip().split("-")
        origin = hub_names[0].strip()
        destination = hub_names[1].strip()
        capacity = 1
        if len(data) == 2:
            key, value = data[1].removesuffix("]").strip().split("=")
            if key == "max_link_capacity":
                capacity = int(value)
        return Connection(self.hubs[origin], self.hubs[destination], capacity)
