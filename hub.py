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
