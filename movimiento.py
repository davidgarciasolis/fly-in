"""Modelo de un movimiento realizado por un dron."""


from conexion import Conexion
from dron import Dron
from hub import Hub


class Movimiento:
    """Representa un movimiento de un dron a un hub o conexión."""

    def __init__(
        self,
        dron: Dron,
        hub: Hub | None = None,
        conexion: Conexion | None = None,
    ) -> None:
        """Guarda el dron, el hub y la conexión del movimiento."""
        self._dron: Dron = dron
        self._hub: Hub | None = hub
        self._conexion: Conexion | None = conexion

    def __lt__(self, otro: "Movimiento") -> bool:
        """Compara movimientos por el identificador de sus drones."""
        identificador = self._dron.get_identificador()
        otro_identificador = otro.get_dron().get_identificador()

        return (identificador < otro_identificador)

    def get_dron(self) -> Dron:
        """Devuelve el dron que realiza el movimiento."""
        return self._dron

    def get_hub(self) -> Hub | None:
        """Devuelve el hub del movimiento."""
        return self._hub

    def get_conexion(self) -> Conexion | None:
        """Devuelve la conexión del movimiento."""
        return self._conexion
