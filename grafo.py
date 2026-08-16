"""Modelo del grafo de hubs."""

from conexion import Conexion
from dron import Dron
from hub import Hub


class Grafo:
    """Agrupa todos los hubs de la simulación."""

    def __init__(self, configuracion: list[str]) -> None:
        """Inicializa y monta el grafo con una configuración válida."""
        self.cantidad_drones: int
        self.start_hub: Hub
        self.end_hub: Hub
        self.hubs: dict[str, Hub] = {}
        self.conexiones: list[Conexion] = []
        self.drones: list[Dron] = []
        self._montar(configuracion)

    def obtener_vecinos(self, hub: Hub) -> list[Hub]:
        """Devuelve los hubs conectados al hub indicado."""
        vecinos: list[Hub] = []

        for conexion in self.conexiones:
            if conexion.origen == hub:
                vecinos.append(conexion.destino)
            elif conexion.destino == hub:
                vecinos.append(conexion.origen)

        return vecinos

    def obtener_hub_dron(self, dron: Dron) -> Hub | None:
        """Devuelve el hub en el que se encuentra un dron."""
        for hub in self.hubs.values():
            if dron in hub.drones:
                return hub

        return None

    def obtener_conexion(
        self, origen: Hub, destino: Hub
    ) -> Conexion | None:
        """Devuelve la conexión bidireccional entre dos hubs."""
        for conexion in self.conexiones:
            if (conexion.origen == origen and conexion.destino == destino):
                return (conexion)
            if (conexion.origen == destino and conexion.destino == origen):
                return (conexion)

        return None

    def _montar(self, configuracion: list[str]) -> None:
        """Monta el grafo a partir de la configuración del mapa."""
        linea: str
        contenido: str
        numero_drones: str
        hub: Hub
        conexion: Conexion
        dron: Dron
        identificador: int

        for linea in configuracion:
            linea = linea.strip()

            if linea.startswith("nb_drones:"):
                numero_drones = linea.removeprefix("nb_drones:")
                numero_drones = numero_drones.strip()
                self.cantidad_drones = int(numero_drones)
            elif linea.startswith("start_hub:"):
                contenido = linea.removeprefix("start_hub:")
                contenido = contenido.strip()
                hub = self._crear_hub(contenido)
                hub.capacidad = self.cantidad_drones
                self.start_hub = hub
                self.hubs[hub.nombre] = hub
            elif linea.startswith("end_hub:"):
                contenido = linea.removeprefix("end_hub:")
                contenido = contenido.strip()
                hub = self._crear_hub(contenido)
                hub.capacidad = self.cantidad_drones
                self.end_hub = hub
                self.hubs[hub.nombre] = hub
            elif linea.startswith("hub:"):
                contenido = linea.removeprefix("hub:")
                contenido = contenido.strip()
                hub = self._crear_hub(contenido)
                self.hubs[hub.nombre] = hub
            elif linea.startswith("connection:"):
                contenido = linea.removeprefix("connection:")
                contenido = contenido.strip()
                conexion = self._crear_conexion(contenido)
                self.conexiones.append(conexion)

        for identificador in range(1, self.cantidad_drones + 1):
            dron = Dron(identificador)
            self.drones.append(dron)
            self.start_hub.drones.append(dron)

    def _crear_hub(self, contenido: str) -> Hub:
        """Crea y devuelve un hub con sus datos obligatorios y opcionales."""
        x: int
        y: int
        capacidad: int
        nombre: str
        tipo_zona: str
        color: str | None
        clave: str
        valor: str
        datos_obligatorios: str
        datos_opcionales: str
        datos: list[str]
        partes_obligatorias: list[str]
        opciones: list[str]
        hub: Hub

        datos = contenido.split("[")
        datos_obligatorios = datos[0]
        partes_obligatorias = datos_obligatorios.split()
        nombre = partes_obligatorias[0]
        x = int(partes_obligatorias[1])
        y = int(partes_obligatorias[2])

        tipo_zona = "normal"
        color = None
        capacidad = 1

        if len(datos) == 2:
            datos_opcionales = datos[1]
            datos_opcionales = datos_opcionales.removesuffix("]")
            opciones = datos_opcionales.split()
            for opcion in opciones:
                clave, valor = opcion.split("=")

                if clave == "zone":
                    tipo_zona = valor
                elif clave == "color":
                    color = valor
                elif clave == "max_drones":
                    capacidad = int(valor)
        hub = Hub(nombre, x, y, tipo_zona, color, capacidad)
        return (hub)

    def _crear_conexion(self, contenido: str) -> Conexion:
        """Crea una conexión con los dos hubs indicados."""
        capacidad: int
        origen: str
        destino: str
        datos_obligatorios: str
        datos_opcionales: str
        clave: str
        valor: str
        datos: list[str]
        nombres_hubs: list[str]
        opcion: list[str]
        hub_origen: Hub
        hub_destino: Hub
        conexion: Conexion

        datos = contenido.split("[")
        datos_obligatorios = datos[0]
        datos_obligatorios = datos_obligatorios.strip()
        nombres_hubs = datos_obligatorios.split("-")
        origen = nombres_hubs[0]
        origen = origen.strip()
        destino = nombres_hubs[1]
        destino = destino.strip()
        hub_origen = self.hubs[origen]
        hub_destino = self.hubs[destino]

        capacidad = 1
        if len(datos) == 2:
            datos_opcionales = datos[1]
            datos_opcionales = datos_opcionales.removesuffix("]")
            datos_opcionales = datos_opcionales.strip()
            opcion = datos_opcionales.split("=")
            clave = opcion[0]
            valor = opcion[1]

            if clave == "max_link_capacity":
                capacidad = int(valor)
        conexion = Conexion(hub_origen, hub_destino, capacidad)
        return (conexion)
