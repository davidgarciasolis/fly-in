"""Modelo de una conexión entre hubs."""

from hub import Hub

class Conexion:
    """Representa una conexión bidireccional entre dos hubs."""

    def __init__(self, origen: Hub, destino: Hub, capacidad: int = 1) -> None:
        """Inicializa una conexión con su capacidad máxima de tránsito."""
        self.origen: Hub = origen
        self.destino: Hub = destino
        self.capacidad: int = capacidad
