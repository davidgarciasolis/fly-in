"""Simulación de movimientos de drones."""

from buscador_rutas import BuscadorRutas
from dron import Dron
from errores import ErrorSimulacion
from grafo import Grafo
from hub import Hub
from movimiento import Movimiento


class Simulador:
    """Coordina los movimientos de los drones en un grafo."""

    def __init__(self, grafo: Grafo) -> None:
        """Prepara el grafo y los costes de las rutas."""
        self.grafo: Grafo = grafo
        self.buscador_rutas = BuscadorRutas(grafo)
        self.costes: dict[str, int] = self.buscador_rutas.calcular_rutas()
        self.movimientos: list[list[Movimiento]] = []

    def ejecutar(self) -> list[list[Movimiento]]:
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
        llegada_drones: list[Dron] = []
        hubs_con_reservas: list[Hub]
        movimientos_turno: list[Movimiento] = []

        self.grafo.limpiar_conexiones()

        hubs_con_reservas = self.grafo.obtener_hubs_con_reservas()
        for hub in hubs_con_reservas:
            reservas = hub.reservas.copy()

            for dron, hub_origen in reservas:
                conexion = self.grafo.obtener_conexion(hub_origen, hub)
                conexion.transita_dron(dron)
                hub.eliminar_reserva(dron, hub_origen)
                hub.entra_dron(dron)
                llegada_drones.append(dron)
                movimiento = Movimiento(
                    dron=dron,
                    hub=hub,
                    conexion=None,
                )
                movimientos_turno.append(movimiento)

        drones = self.grafo.drones
        for dron in drones:
            if dron in llegada_drones:
                continue

            hub_actual = self.grafo.obtener_hub_dron(dron)

            if hub_actual is None:
                continue

            if hub_actual == self.grafo.end_hub:
                continue

            movimiento = self.mover_dron(dron, hub_actual)

            if movimiento is not None:
                movimientos_turno.append(movimiento)

        if not movimientos_turno:
            raise ErrorSimulacion("El mapa no es posible de realizar.")

        self.movimientos.append(movimientos_turno)

    def mover_dron(
        self, dron: Dron, hub_actual: Hub
    ) -> Movimiento | None:
        """Mueve un dron y devuelve el movimiento realizado."""
        siguiente_hub = self.siguiente_movimiento(hub_actual)

        if siguiente_hub is None:
            return None

        conexion = self.grafo.obtener_conexion(hub_actual, siguiente_hub)
        conexion.transita_dron(dron)
        hub_actual.sale_dron(dron)

        if siguiente_hub.tipo_zona == "restricted":
            siguiente_hub.crear_reserva(dron, hub_actual)
            movimiento = Movimiento(
                dron=dron,
                hub=None,
                conexion=conexion,
            )
        else:
            siguiente_hub.entra_dron(dron)
            movimiento = Movimiento(
                dron=dron,
                hub=siguiente_hub,
                conexion=None,
            )

        return movimiento

    def siguiente_movimiento(self, hub_actual: Hub) -> Hub | None:
        """Devuelve el mejor hub al que puede moverse un dron."""
        coste_actual = self.costes[hub_actual.nombre]
        vecinos_validos: list[Hub] = []

        for vecino in self.grafo.obtener_vecinos(hub_actual):
            if vecino.tipo_zona == "blocked":
                continue

            if self.costes[vecino.nombre] >= coste_actual:
                continue

            if vecino.esta_lleno():
                continue

            conexion = self.grafo.obtener_conexion(hub_actual, vecino)
            if conexion.esta_llena():
                continue

            vecinos_validos.append(vecino)

        if not vecinos_validos:
            return None

        menor_coste = self.costes[vecinos_validos[0].nombre]

        for vecino in vecinos_validos:
            if self.costes[vecino.nombre] < menor_coste:
                menor_coste = self.costes[vecino.nombre]

        for vecino in vecinos_validos:
            es_menor_coste = self.costes[vecino.nombre] == menor_coste
            if es_menor_coste and vecino.tipo_zona == "priority":
                return vecino

        for vecino in vecinos_validos:
            if self.costes[vecino.nombre] == menor_coste:
                return vecino

        return None
