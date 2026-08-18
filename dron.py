"""Modelo de un dron."""


class Dron:
    """Representa un dron de la simulación."""

    def __init__(self, identificador: int) -> None:
        """Inicializa un dron con su identificador único."""
        self.identificador: int = identificador

    def get_identificador(self) -> int:
        """Devuelve el identificador único del dron."""
        return self.identificador
