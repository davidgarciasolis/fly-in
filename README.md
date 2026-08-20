# Fly-In

## Description

Fly-In is a Python drone-routing simulator. It moves a group of drones from a
`start_hub` to an `end_hub` through a custom graph of hubs and connections.
The simulator considers path costs, hub capacity, connection capacity,
restricted zones, blocked zones, and priority zones.

Map files are supplied when the program is executed or evaluated; they are
not included in this repository.

## Requirements

- Python 3.10 or later.
- `flake8` and `mypy` are required only for linting.

Use a virtual environment before installing development tools so that system
Python packages are not modified:

```bash
python3 -m venv .venv
. .venv/bin/activate
make install
```

## Instructions

Run the program by passing a map file:

```bash
python3 fly-in.py path/to/map.txt
```

Use `--color` to enable ANSI colours for movements that arrive at hubs:

```bash
python3 fly-in.py path/to/map.txt --color
```

The Makefile provides the same commands:

```bash
make run MAPA=path/to/map.txt
make debug MAPA=path/to/map.txt
```

`make debug` starts Python's `pdb` debugger. Useful commands are `n` for the
next line, `s` to enter a method, `p variable` to print a value, `c` to
continue, and `q` to quit.

## Algorithm Explanation

`BuscadorRutas` calculates the minimum cost from every hub to the end hub. It
starts at the end hub with cost `0`, then visits connected hubs backwards. A
hub is updated when a cheaper cost is found and is added to the pending list
again. Blocked hubs are ignored. Entering a normal or priority hub costs one
turn; entering a restricted hub costs two turns.

Before the simulation starts, `Simulador` orders hubs by ascending route
cost. Hubs closest to the end hub are therefore processed first in each turn.
When a drone leaves one of those hubs, its capacity is released before drones
from more distant hubs try to enter it.

For each drone, the simulator selects a connected hub that:

- is not blocked;
- has a lower route cost than the current hub;
- has free hub capacity;
- has a connection with free capacity.

If several valid neighbours have the same minimum cost, a `priority` hub is
selected first. When a drone moves towards a restricted hub, the simulator
creates a reservation for that hub. The drone reaches the reserved hub on the
following turn, so it cannot wait indefinitely in a connection.

If a turn produces no movement while drones are still undelivered, the
simulation stops instead of looping forever.

At the end of each turn, its movements are ordered by drone identifier and
printed immediately. Previous turns are not kept in memory.

## Visual Representation

The `--color` flag enables ANSI terminal colours. When a movement ends in a
hub, its text uses the colour specified by that hub's `color` metadata. For
example, a blue hub is displayed in blue. Connection movements remain
uncoloured because connections do not have their own colour.

This makes the route and the current destination of every moving drone easier
to distinguish while keeping the required text output format.

## Example Input and Expected Output

Example map file, `example.txt`:

```text
nb_drones: 2
start_hub: start 0 0 [color=green]
hub: waypoint 1 0 [color=blue]
end_hub: goal 2 0 [color=red]
connection: start-waypoint
connection: waypoint-goal
```

Command:

```bash
python3 fly-in.py example.txt
```

Expected output:

```text
D1-waypoint
D1-goal D2-waypoint
D2-goal
```

Each line is a turn. Movements are ordered by drone identifier and separated
by spaces. A regular movement has the format `D<ID>-<hub>`. A drone travelling
towards a restricted hub is shown with its connection, for example:

```text
D2-start-restricted_hub
```

If no drone can move, the program prints:

```text
El mapa no es posible de realizar.
```

## Zone Rules

- `normal` zones cost one turn.
- `priority` zones cost one turn and win a cost tie.
- `restricted` zones cost two turns.
- `blocked` zones cannot be entered.
- Hub capacity uses `max_drones`; connection capacity uses
  `max_link_capacity`.

## Project Structure

| File | Responsibility |
| --- | --- |
| `fly-in.py` | Program entry point and command-line argument handling. |
| `parser_mapa.py` | Map file reading, validation, and error reporting. |
| `grafo.py` | Graph, hubs, connections, and drones creation. |
| `buscador_rutas.py` | Minimum-cost calculation to the destination. |
| `simulador.py` | Turn execution, reservations, and movements. |
| `hub.py` | Hub state, capacity, and reservations. |
| `conexion.py` | Connection capacity and drones in transit. |
| `movimiento.py` | Data for one drone movement. |
| `render.py` | Output construction, sorting, and colours. |

## Makefile

| Rule | Action |
| --- | --- |
| `make install` | Installs `flake8` and `mypy` in the active virtual environment. |
| `make run MAPA=path/to/map.txt` | Runs the simulator. |
| `make debug MAPA=path/to/map.txt` | Runs the simulator with `pdb`. |
| `make clean` | Removes Python and mypy cache directories. |
| `make lint` | Runs `flake8` and mypy with the required options. |
| `make lint-strict` | Runs the optional strict checks. |
