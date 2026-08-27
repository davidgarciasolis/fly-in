"""Minimum-cost route search for drone simulations."""

from graph import Graph
from hub import Hub


class RouteFinder:
    """Calculate the cost from every hub to the destination hub."""

    def __init__(self, graph: Graph) -> None:
        """Store the graph used for route calculations."""
        self.graph: Graph = graph

    def calculate_routes(self) -> dict[str, int]:
        """Return the minimum route cost for every hub."""
        costs: dict[str, int] = {}
        pending_hubs: list[Hub] = [self.graph.end_hub]

        for hub in self.graph.hubs.values():
            costs[hub.name] = 9999
        costs[self.graph.end_hub.name] = 0

        while pending_hubs:
            current_hub = pending_hubs.pop(0)
            neighbors = self.graph.get_neighbors(current_hub)
            for neighbor in neighbors:
                if neighbor.zone_type == "blocked":
                    continue
                new_cost = costs[current_hub.name] + current_hub.get_cost()
                if new_cost < costs[neighbor.name]:
                    costs[neighbor.name] = new_cost
                    pending_hubs.append(neighbor)

        return costs
