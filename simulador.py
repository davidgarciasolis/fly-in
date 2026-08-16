"""Simulación de movimientos de drones."""

from buscador_rutas import BuscadorRutas
from dron import Dron
from grafo import Grafo
from hub import Hub


class Simulador:
    """Coordina los movimientos de los drones en un grafo."""

    def __init__(self, grafo: Grafo) -> None:
        """Prepara el grafo y los costes de las rutas."""
        self.grafo: Grafo = grafo
        self.buscador_rutas = BuscadorRutas(grafo)
        self.costes: dict[str, int] = self.buscador_rutas.calcular_rutas()
        self.movimientos: list[list[str]] = []

    def ejecutar(self) -> list[list[str]]:
        """Ejecuta turnos y devuelve todos los movimientos realizados."""
        while not self.llegaron_todos():
            self.ejecutar_turno()

        return self.movimientos

    def llegaron_todos(self) -> bool:
        """Indica si todos los drones llegaron al hub final."""
        return len(self.grafo.end_hub.drones) == len(self.grafo.drones)

    def ejecutar_turno(self) -> None:
        """Intenta mover cada dron una sola vez."""
        drones: list[Dron]
        movimientos_turno: list[str] = []

        drones = self.grafo.drones
        for dron in drones:
            hub_actual = self.grafo.obtener_hub_dron(dron)

            if hub_actual is None:
                continue

            if hub_actual == self.grafo.end_hub:
                continue

            movimiento = self.mover_dron(dron, hub_actual)

            if movimiento is not None:
                movimientos_turno.append(movimiento)

        self.movimientos.append(movimientos_turno)

    def mover_dron(self, dron: Dron, hub_actual: Hub) -> str | None:
        """Mueve un dron y devuelve el movimiento realizado."""
        siguiente_hub = self.siguiente_movimiento(hub_actual)

        if siguiente_hub is None:
            return None

        hub_actual.drones.remove(dron)
        siguiente_hub.drones.append(dron)
        movimiento = f"D{dron.identificador}-{siguiente_hub.nombre}"

        return (movimiento)

    def siguiente_movimiento(self, hub_actual: Hub) -> Hub | None:
        """Devuelve el mejor hub al que puede moverse un dron."""
        mejor_hub: Hub | None = None

        for vecino in self.grafo.obtener_vecinos(hub_actual):
            if vecino.tipo_zona == "blocked":
                continue

            if vecino.esta_lleno():
                continue

            if mejor_hub is None:
                mejor_hub = vecino
            elif self.costes[vecino.nombre] < self.costes[mejor_hub.nombre]:
                mejor_hub = vecino

        return mejor_hub
