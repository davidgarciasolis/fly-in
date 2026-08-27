"""Drone movement simulation engine."""

from route_finder import RouteFinder
from drone import Drone
from errors import SimulationError
from graph import Graph
from hub import Hub
from movement import Movement
from renderer import Renderer


class Simulator:
    """Coordinate drone movements through a graph."""

    def __init__(self, graph: Graph, use_color: bool) -> None:
        """Prepare the graph, route costs, and movement renderer."""
        self.graph: Graph = graph
        self.renderer: Renderer = Renderer(use_color)
        self.route_finder = RouteFinder(graph)
        self.costs: dict[str, int] = self.route_finder.calculate_routes()
        self.hubs: list[Hub] = []

    def run(self) -> None:
        """Run turns until all drones reach the destination hub."""
        self.hubs = list(self.graph.hubs.values())
        self.hubs.sort(key=self.get_hub_cost)
        start_hub = self.graph.start_hub
        if self.costs[start_hub.name] == 9999:
            raise SimulationError("El mapa no es posible de realizar.")
        while not self.have_all_arrived():
            self.run_turn()

    def get_hub_cost(self, hub: Hub) -> int:
        """Return the route cost of a hub."""
        return self.costs[hub.name]

    def have_all_arrived(self) -> bool:
        """Return whether every drone has reached the end hub."""
        return len(self.graph.end_hub.drones) == len(self.graph.drones)

    def run_turn(self) -> None:
        """Move every eligible drone at most once during a turn."""
        moved_drones: set[Drone] = set()
        turn_movements: list[Movement] = []
        self.graph.clear_connections()

        hubs_with_reservations = self.graph.get_hubs_with_reservations()
        for hub in hubs_with_reservations:
            reservations = hub.reservations.copy()
            for drone, origin_hub in reservations:
                connection = self.graph.get_connection(origin_hub, hub)
                connection.transit_drone(drone)
                hub.remove_reservation(drone, origin_hub)
                hub.enter_drone(drone)
                moved_drones.add(drone)
                turn_movements.append(Movement(drone=drone, hub=hub))

        for hub in self.hubs:
            drones = hub.drones.copy()
            for drone in drones:
                if drone in moved_drones or hub == self.graph.end_hub:
                    continue
                movement = self.move_drone(drone, hub)
                if movement is None:
                    break
                turn_movements.append(movement)
                moved_drones.add(drone)

        if not turn_movements:
            raise SimulationError("El mapa no es posible de realizar.")
        self.renderer.print_movements(turn_movements)

    def move_drone(
        self, drone: Drone, current_hub: Hub
    ) -> Movement | None:
        """Move a drone from its current hub and return its movement."""
        next_hub = self.get_next_hub(current_hub)
        if next_hub is None:
            return None
        connection = self.graph.get_connection(current_hub, next_hub)
        connection.transit_drone(drone)
        current_hub.leave_drone(drone)
        if next_hub.zone_type == "restricted":
            next_hub.create_reservation(drone, current_hub)
            return Movement(drone=drone, connection=connection)
        next_hub.enter_drone(drone)
        return Movement(drone=drone, hub=next_hub)

    def get_next_hub(self, current_hub: Hub) -> Hub | None:
        """Return the best available next hub for a drone."""
        current_cost = self.costs[current_hub.name]
        valid_neighbors: list[Hub] = []
        for neighbor in self.graph.get_neighbors(current_hub):
            if neighbor.zone_type == "blocked":
                continue
            if self.costs[neighbor.name] > current_cost or neighbor.is_full():
                continue
            connection = self.graph.get_connection(current_hub, neighbor)
            if not connection.is_full():
                valid_neighbors.append(neighbor)
        if not valid_neighbors:
            return None
        lowest_cost = min(self.costs[hub.name] for hub in valid_neighbors)
        for hub in valid_neighbors:
            if (
                self.costs[hub.name] == lowest_cost
                and hub.zone_type == "priority"
            ):
                return hub
        return next(
            hub for hub in valid_neighbors
            if self.costs[hub.name] == lowest_cost
        )
