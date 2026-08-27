"""Command-line entry point for the Fly-In simulator."""

import sys

from errors import MapConfigurationError, SimulationError
from graph import Graph
from map_parser import MapParser
from simulator import Simulator


def main() -> int:
    """Parse command-line arguments and run the simulation."""
    use_color = False
    if len(sys.argv) < 2:
        print("Uso: python3 fly-in.py <mapa> [--color]")
        return 1
    for option in sys.argv[2:]:
        if option == "--color" and not use_color:
            use_color = True
        else:
            print("Las opciones admitidas son: --color.")
            return 1

    file_path = sys.argv[1]
    parser = MapParser(file_path)
    try:
        configuration = parser.read_configuration()
        graph = Graph(configuration)
        simulator = Simulator(graph, use_color)
        simulator.run()
    except (MapConfigurationError, SimulationError) as error:
        print(error)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
