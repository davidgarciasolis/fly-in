"""Modelo de una conexión entre hubs."""

from dron import Dron
from hub import Hub


class Conexion:
    """Representa una conexión bidireccional entre dos hubs."""

    def __init__(self, origen: Hub, destino: Hub, capacidad: int = 1) -> None:
        """Inicializa una conexión con su capacidad máxima de tránsito."""
        self.origen: Hub = origen
        self.destino: Hub = destino
        self.capacidad: int = capacidad
        self.drones_en_transito: list[Dron] = []

    def esta_llena(self) -> bool:
        """Indica si la conexión ha alcanzado su capacidad máxima."""
        return len(self.drones_en_transito) >= self.capacidad

    def transita_dron(self, dron: Dron) -> None:
        """Añade un dron a los drones en tránsito."""
        self.drones_en_transito.append(dron)

    def limpiar_drones_en_transito(self) -> None:
        """Elimina todos los drones en tránsito de la conexión."""
        self.drones_en_transito.clear()
