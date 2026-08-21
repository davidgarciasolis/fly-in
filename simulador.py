"""Simulación de movimientos de drones."""

from buscador_rutas import BuscadorRutas
from dron import Dron
from errores import ErrorSimulacion
from grafo import Grafo
from hub import Hub
from movimiento import Movimiento
from render import Render


class Simulador:
    """Coordina los movimientos de los drones en un grafo."""

    def __init__(self, grafo: Grafo, usar_color: bool) -> None:
        """Prepara el grafo y los costes de las rutas."""
        self.grafo: Grafo = grafo
        self.render: Render = Render(usar_color)
        self.buscador_rutas = BuscadorRutas(grafo)
        self.costes: dict[str, int] = self.buscador_rutas.calcular_rutas()
        self.hubs: list[Hub] = []

    def ejecutar(self) -> None:
        """Ejecuta turnos y devuelve todos los movimientos realizados."""
        self.hubs = list(self.grafo.hubs.values())
        self.hubs.sort(key=self.obtener_coste_hub)

        while not self.llegaron_todos():
            self.ejecutar_turno()

    def obtener_coste_hub(self, hub: Hub) -> int:
        """Devuelve el coste de un hub hasta el hub final."""
        return self.costes[hub.nombre]

    def llegaron_todos(self) -> bool:
        """Indica si todos los drones llegaron al hub final."""
        return len(self.grafo.end_hub.drones) == len(self.grafo.drones)

    def ejecutar_turno(self) -> None:
        """Intenta mover cada dron una sola vez."""
        movimiento: Movimiento | None
        drones: list[Dron]
        drones_movidos: set[Dron] = set()
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
                drones_movidos.add(dron)
                movimiento = Movimiento(
                    dron=dron,
                    hub=hub,
                    conexion=None,
                )
                movimientos_turno.append(movimiento)

        for hub in self.hubs:
            drones = hub.drones.copy()
            for dron in drones:
                if dron in drones_movidos:
                    continue

                if hub == self.grafo.end_hub:
                    continue

                movimiento = self.mover_dron(dron, hub)

                if movimiento is None:
                    break
                else:
                    movimientos_turno.append(movimiento)
                    drones_movidos.add(dron)

        if not movimientos_turno:
            raise ErrorSimulacion("El mapa no es posible de realizar.")

        self.render.imprimir_movimientos(movimientos_turno)

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
