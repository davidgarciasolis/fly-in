"""Modelo de un hub."""

from dron import Dron


class Hub:
    """Representa una zona del grafo."""

    def __init__(
        self,
        nombre: str,
        x: int,
        y: int,
        tipo_zona: str = "normal",
        color: str | None = None,
        capacidad: int = 1,
    ) -> None:
        """Inicializa un hub sin conexiones ni drones."""
        self.nombre: str = nombre
        self.x: int = x
        self.y: int = y
        self.tipo_zona: str = tipo_zona
        self.color: str | None = color
        self.capacidad: int = capacidad
        self.drones: list[Dron] = []
        self.reservas: list[Dron] = []

    def crear_reserva(self, dron: Dron) -> None:
        """Reserva una plaza para un dron en el hub."""
        self.reservas.append(dron)

    def eliminar_reserva(self, dron: Dron) -> None:
        """Elimina la reserva de un dron en el hub."""
        self.reservas.remove(dron)

    def entra_dron(self, dron: Dron) -> None:
        """Añade un dron al hub."""
        self.drones.append(dron)

    def sale_dron(self, dron: Dron) -> None:
        """Elimina un dron del hub."""
        self.drones.remove(dron)

    def obtener_coste(self) -> int:
        """Devuelve el coste necesario para entrar en este hub."""
        if self.tipo_zona == "restricted":
            return 2

        return 1

    def esta_lleno(self) -> bool:
        """Indica si el hub ha alcanzado su capacidad máxima."""
        ocupacion = len(self.drones) + len(self.reservas)
        return ocupacion >= self.capacidad
