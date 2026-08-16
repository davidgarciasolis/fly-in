"""Modelo de un dron."""

from movimiento import Movimiento


class Dron:
    """Representa un dron de la simulación."""

    def __init__(self, identificador: int) -> None:
        """Inicializa un dron con su identificador único."""
        self.identificador: int = identificador
        self.movimientos: list[Movimiento] = []
