"""Map configuration file reader and validator."""

from pathlib import Path

from errors import MapConfigurationError as ErrorConfiguracionMapa


class MapParser:
    """Load and validate map configuration files."""

    def __init__(self, file_path: str) -> None:
        """Store the path of the map file to load."""
        self.file_path = Path(file_path)

    def read_configuration(self) -> list[str]:
        """Read, validate, and return the map configuration lines."""
        file_lines = self._read_file()
        lines = self._remove_comments_and_empty_lines(file_lines)
        line_number, first_line = lines[0]
        first_line = first_line.strip()
        try:
            self._validate_drone_count(first_line)
        except ErrorConfiguracionMapa as error:
            message = f"Línea {line_number}: {error}"
            raise ErrorConfiguracionMapa(message) from error

        configuration_lines = [first_line]
        start_count = 0
        end_count = 0
        hub_names: list[str] = []
        connections: list[tuple[str, str]] = []
        for line_number, line in lines[1:]:
            line = line.strip()
            try:
                if line.startswith("start_hub:"):
                    start_count += 1
                    hub_content = line.removeprefix("start_hub:").strip()
                    self._validate_hub(hub_content, hub_names)
                elif line.startswith("hub:"):
                    hub_content = line.removeprefix("hub:").strip()
                    self._validate_hub(hub_content, hub_names)
                elif line.startswith("end_hub:"):
                    end_count += 1
                    hub_content = line.removeprefix("end_hub:").strip()
                    self._validate_hub(hub_content, hub_names)
                elif line.startswith("connection:"):
                    connection_content = line.removeprefix(
                        "connection:"
                    ).strip()
                    self._validate_connection(
                        connection_content, hub_names, connections
                    )
                else:
                    raise ErrorConfiguracionMapa(
                        "Las líneas deben empezar por start_hub:, hub:, "
                        "end_hub: o connection:."
                    )
            except ErrorConfiguracionMapa as error:
                raise ErrorConfiguracionMapa(
                    f"Línea {line_number}: {error}"
                ) from error
            configuration_lines.append(line)

        if start_count != 1 or end_count != 1:
            raise ErrorConfiguracionMapa(
                "El mapa debe tener exactamente un start_hub y un end_hub."
            )
        return configuration_lines

    def _read_file(self) -> list[str]:
        """Read all lines from the configured map file."""
        if not self.file_path.is_file():
            raise ErrorConfiguracionMapa(
                f"El archivo de mapa no existe: {self.file_path}"
            )
        try:
            with self.file_path.open("r") as file:
                return file.readlines()
        except (OSError, UnicodeDecodeError) as error:
            raise ErrorConfiguracionMapa(
                f"No se puede leer el mapa: {self.file_path}"
            ) from error

    def _remove_comments_and_empty_lines(
        self, file_lines: list[str]
    ) -> list[tuple[int, str]]:
        """Remove comments and blank lines while retaining line numbers."""
        lines: list[tuple[int, str]] = []
        for index, line in enumerate(file_lines, start=1):
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith("#"):
                lines.append((index, line))
        if not lines:
            raise ErrorConfiguracionMapa("El archivo de mapa está vacío.")
        return lines

    def _validate_drone_count(self, first_line: str) -> None:
        """Validate the map's declared number of drones."""
        if not first_line.startswith("nb_drones:"):
            raise ErrorConfiguracionMapa(
                "La primera línea debe empezar por 'nb_drones:'."
            )
        parts = first_line.split(":")
        if len(parts) != 2:
            raise ErrorConfiguracionMapa(
                "La primera línea debe tener el formato: nb_drones: <número>."
            )
        drone_count = parts[1].strip()
        if not drone_count.isdigit() or int(drone_count) <= 0:
            raise ErrorConfiguracionMapa(
                "El número de drones debe ser un entero positivo."
            )

    def _validate_hub(self, line: str, hub_names: list[str]) -> None:
        """Validate the content of a hub declaration."""
        parts = line.split("[")
        if len(parts) > 2:
            raise ErrorConfiguracionMapa(
                "Un hub solo puede tener un bloque de opciones."
            )
        required_parts = parts[0].strip().split()
        self.validate_required_hub_data(required_parts, hub_names)
        if len(parts) == 2:
            optional_data = parts[1].strip()
            if not optional_data.endswith("]"):
                raise ErrorConfiguracionMapa(
                    "Las opciones de un hub deben terminar con ']'."
                )
            self.validate_optional_hub_data(
                optional_data.removesuffix("]").strip()
            )

    def validate_required_hub_data(
        self, required_parts: list[str], hub_names: list[str]
    ) -> None:
        """Validate a hub name and its required coordinates."""
        if len(required_parts) != 3:
            raise ErrorConfiguracionMapa(
                "Un hub debe tener nombre, posición x y posición y."
            )
        name, x_position, y_position = required_parts
        if "-" in name:
            raise ErrorConfiguracionMapa(
                "El nombre de un hub no puede contener guiones."
            )
        if name in hub_names:
            raise ErrorConfiguracionMapa(
                "El nombre de cada hub debe ser único."
            )
        try:
            int(x_position)
            int(y_position)
        except ValueError as error:
            raise ErrorConfiguracionMapa(
                "Las posiciones x e y de un hub deben ser números enteros."
            ) from error
        hub_names.append(name)

    def validate_optional_hub_data(self, optional_data: str) -> None:
        """Validate the optional settings for a hub."""
        if not optional_data:
            raise ErrorConfiguracionMapa(
                "El bloque de opciones de un hub no puede estar vacío."
            )
        if "[" in optional_data or "]" in optional_data:
            raise ErrorConfiguracionMapa(
                "El bloque de opciones de un hub tiene corchetes no válidos."
            )
        valid_zones = ["normal", "blocked", "restricted", "priority"]
        used_keys: list[str] = []
        for option in optional_data.split():
            option_parts = option.split("=")
            if len(option_parts) != 2:
                raise ErrorConfiguracionMapa(
                    "Las opciones de un hub deben tener formato clave=valor."
                )
            key, value = option_parts
            if key in used_keys:
                raise ErrorConfiguracionMapa(
                    "Una opción de un hub no puede repetirse."
                )
            used_keys.append(key)
            if key == "zone" and value not in valid_zones:
                raise ErrorConfiguracionMapa("El tipo de zona no es válido.")
            if key == "color" and not value:
                raise ErrorConfiguracionMapa("El color no puede estar vacío.")
            if key == "max_drones" and (
                not value.isdigit() or int(value) <= 0
            ):
                raise ErrorConfiguracionMapa(
                    "max_drones debe ser un entero positivo."
                )
            if key not in ("zone", "color", "max_drones"):
                raise ErrorConfiguracionMapa("La opción del hub no es válida.")

    def _validate_connection(
        self,
        connection_content: str,
        hub_names: list[str],
        connections: list[tuple[str, str]],
    ) -> None:
        """Validate the content of a connection declaration."""
        parts = connection_content.split("[")
        if len(parts) > 2:
            raise ErrorConfiguracionMapa(
                "Una conexión solo puede tener un bloque de opciones."
            )
        self.validate_required_connection_data(
            parts[0].strip(), hub_names, connections
        )
        if len(parts) == 2:
            optional_data = parts[1].strip()
            if not optional_data.endswith("]"):
                raise ErrorConfiguracionMapa(
                    "Las opciones de una conexión deben terminar con ']'."
                )
            self.validate_optional_connection_data(
                optional_data.removesuffix("]").strip()
            )

    def validate_required_connection_data(
        self,
        required_data: str,
        hub_names: list[str],
        connections: list[tuple[str, str]],
    ) -> None:
        """Validate a connection's origin, destination, and uniqueness."""
        parts = required_data.split("-")
        if len(parts) != 2:
            raise ErrorConfiguracionMapa(
                "Una conexión debe tener el formato origen-destino."
            )
        origin, destination = (part.strip() for part in parts)
        if not origin or not destination:
            raise ErrorConfiguracionMapa(
                "El origen y el destino de una conexión no pueden "
                "estar vacíos."
            )
        if origin == destination:
            raise ErrorConfiguracionMapa(
                "El origen y el destino de una conexión deben ser distintos."
            )
        if not hub_names:
            raise ErrorConfiguracionMapa(
                "No puede haber conexiones sin hubs definidos."
            )
        if origin not in hub_names or destination not in hub_names:
            raise ErrorConfiguracionMapa(
                "Una conexión solo puede usar hubs definidos previamente."
            )
        if (
            (origin, destination) in connections
            or (destination, origin) in connections
        ):
            raise ErrorConfiguracionMapa("Una conexión no puede repetirse.")
        connections.append((origin, destination))

    def validate_optional_connection_data(self, optional_data: str) -> None:
        """Validate the optional settings for a connection."""
        if not optional_data:
            raise ErrorConfiguracionMapa(
                "El bloque de opciones de una conexión no puede estar vacío."
            )
        if "[" in optional_data or "]" in optional_data:
            raise ErrorConfiguracionMapa(
                "El bloque de opciones de una conexión tiene "
                "corchetes no válidos."
            )
        parts = optional_data.split("=")
        if len(parts) != 2:
            raise ErrorConfiguracionMapa(
                "La opción de una conexión debe tener formato clave=valor."
            )
        key, value = parts
        if key != "max_link_capacity":
            raise ErrorConfiguracionMapa(
                "La única opción de una conexión es max_link_capacity."
            )
        if not value.isdigit() or int(value) <= 0:
            raise ErrorConfiguracionMapa(
                "max_link_capacity debe ser un entero positivo."
            )
