"""Modelo de un movimiento realizado por un dron."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hub import Hub


class Movimiento:
    """Representa un movimiento de un dron durante la simulación."""

    def __init__(
        self,
        origen: "Hub",
        destino: "Hub",
        turno_inicio: int,
        duracion: int,
    ) -> None:
        """Guarda los datos de un movimiento entre dos hubs."""
        self.origen: Hub = origen
        self.destino: Hub = destino
        self.turno_inicio: int = turno_inicio
        self.duracion: int = duracion
