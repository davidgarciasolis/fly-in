"""Búsqueda de rutas para la simulación de drones."""

from grafo import Grafo
from hub import Hub


class BuscadorRutas:
    """Calcula rutas entre los hubs de un grafo."""

    def __init__(self, grafo: Grafo) -> None:
        """Guarda el grafo sobre el que se calcularán las rutas."""
        self.grafo: Grafo = grafo

    def calcular_rutas(self) -> dict[str, int]:
        """Calcula el coste mínimo de cada hub hasta el hub final."""
        costes: dict[str, int] = {}
        hubs_pendientes: list[Hub] = [self.grafo.end_hub]

        for hub in self.grafo.hubs.values():
            costes[hub.nombre] = 9999

        costes[self.grafo.end_hub.nombre] = 0

        while hubs_pendientes:
            hub_actual = hubs_pendientes.pop(0)

            vecinos = self.grafo.obtener_vecinos(hub_actual)
            for vecino in vecinos:
                if vecino.tipo_zona == "blocked":
                    continue

                coste_nuevo = (
                    costes[hub_actual.nombre] + hub_actual.obtener_coste()
                )
                if coste_nuevo < costes[vecino.nombre]:
                    costes[vecino.nombre] = coste_nuevo
                    hubs_pendientes.append(vecino)

        return (costes)
