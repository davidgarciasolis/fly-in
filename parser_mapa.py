"""Lectura inicial de archivos de configuración de mapas."""

from pathlib import Path

from errores import ErrorConfiguracionMapa


class ParserMapa:
    """Carga el contenido de un archivo de configuración de mapa."""

    def __init__(self, ruta_archivo: str) -> None:
        """Guarda la ruta del archivo que se quiere cargar."""
        self.ruta_archivo = Path(ruta_archivo)

    def leer_configuracion(self) -> list[str]:
        """Lee el archivo de mapa y devuelve sus líneas comprobadas."""
        start: int
        end: int
        i: int
        numero_linea: int
        primera_linea: str
        linea: str
        contenido_hub: str
        contenido_conexion: str
        lineas_archivo: list[str]
        lineas: list[tuple[int, str]]
        lineas_configuracion: list[str]
        nombres_hubs: list[str]
        conexiones: list[tuple[str, str]]

        lineas_archivo = self._leer_archivo()
        lineas = self._quitar_comentarios_y_lineas_vacias(lineas_archivo)

        numero_linea, primera_linea = lineas[0]
        primera_linea = primera_linea.strip()
        try:
            self._validar_numero_drones(primera_linea)
        except ErrorConfiguracionMapa as error:
            mensaje = f"Línea {numero_linea}: {error}"
            raise ErrorConfiguracionMapa(mensaje) from error

        lineas_configuracion = []
        lineas_configuracion.append(primera_linea)
        start = 0
        end = 0
        nombres_hubs = []
        conexiones = []

        for i in range(1, len(lineas)):
            numero_linea, linea = lineas[i]
            linea = linea.strip()

            try:
                if linea.startswith("start_hub:"):
                    start += 1
                    contenido_hub = linea.removeprefix("start_hub:")
                    contenido_hub = contenido_hub.strip()
                    self._validar_hub(contenido_hub, nombres_hubs)
                elif linea.startswith("hub:"):
                    contenido_hub = linea.removeprefix("hub:")
                    contenido_hub = contenido_hub.strip()
                    self._validar_hub(contenido_hub, nombres_hubs)
                elif linea.startswith("end_hub:"):
                    end += 1
                    contenido_hub = linea.removeprefix("end_hub:")
                    contenido_hub = contenido_hub.strip()
                    self._validar_hub(contenido_hub, nombres_hubs)
                elif linea.startswith("connection:"):
                    contenido_conexion = linea.removeprefix("connection:")
                    contenido_conexion = contenido_conexion.strip()
                    self._validar_conexion(
                        contenido_conexion, nombres_hubs, conexiones
                    )
                else:
                    raise ErrorConfiguracionMapa(
                        "Las líneas deben empezar por start_hub:, hub:, "
                        "end_hub: o connection:."
                    )
            except ErrorConfiguracionMapa as error:
                mensaje = f"Línea {numero_linea}: {error}"
                raise ErrorConfiguracionMapa(mensaje) from error

            lineas_configuracion.append(linea)

        if start != 1 or end != 1:
            raise ErrorConfiguracionMapa(
                "El mapa debe tener exactamente un start_hub y un end_hub."
            )

        return (lineas_configuracion)

    def _leer_archivo(self) -> list[str]:
        """Lee todas las líneas del archivo de mapa."""
        mensaje: str
        lineas_archivo: list[str]

        if not self.ruta_archivo.is_file():
            mensaje = f"El archivo de mapa no existe: {self.ruta_archivo}"
            raise ErrorConfiguracionMapa(mensaje)

        try:
            with self.ruta_archivo.open("r") as archivo:
                lineas_archivo = archivo.readlines()
        except (OSError, UnicodeDecodeError) as error:
            mensaje = f"No se puede leer el archivo de mapa: {self.ruta_archivo}"
            raise ErrorConfiguracionMapa(mensaje)

        return lineas_archivo

    def _quitar_comentarios_y_lineas_vacias(
        self, lineas_archivo: list[str]
    ) -> list[tuple[int, str]]:
        """Elimina comentarios y líneas vacías conservando su número."""
        i: int
        numero_linea: int
        linea: str
        sin_espacios: str
        lineas: list[tuple[int, str]]
        es_comentario: bool

        lineas = []

        for i in range(len(lineas_archivo)):
            numero_linea = i + 1
            linea = lineas_archivo[i]
            sin_espacios = linea.strip()
            es_comentario = sin_espacios.startswith("#")
            if sin_espacios and not es_comentario:
                lineas.append((numero_linea, linea))

        if not lineas:
            raise ErrorConfiguracionMapa("El archivo de mapa está vacío.")
        return lineas

    def _validar_numero_drones(self, primera_linea: str) -> None:
        """Comprueba que la primera línea indique un número válido de drones."""
        nombre: str
        numero_drones: str
        partes: list[str]

        partes = primera_linea.split(":")
        if len(partes) != 2:
            raise ErrorConfiguracionMapa(
                "La primera línea debe tener el formato: nb_drones: <número>."
            )

        nombre = partes[0].strip()
        numero_drones = partes[1].strip()
        if nombre != "nb_drones":
            raise ErrorConfiguracionMapa(
                "La primera línea debe empezar por 'nb_drones:'."
            )

        if not numero_drones.isdigit() or int(numero_drones) <= 0:
            raise ErrorConfiguracionMapa(
                "El número de drones debe ser un entero positivo."
            )

    def _validar_hub(self, linea: str, nombres_hubs: list[str]) -> None:
        """Comprueba el contenido de una línea de hub."""
        datos_obligatorios: str
        datos_opcionales: str
        partes: list[str]
        partes_obligatorias: list[str]

        partes = linea.split("[")
        if len(partes) > 2:
            raise ErrorConfiguracionMapa(
                "Un hub solo puede tener un bloque de opciones."
            )

        datos_obligatorios = partes[0]
        datos_obligatorios = datos_obligatorios.strip()

        partes_obligatorias = datos_obligatorios.split()
        self.validar_datos_obligatorios_hub(partes_obligatorias, nombres_hubs)

        if len(partes) == 2:
            datos_opcionales = partes[1]
            datos_opcionales = datos_opcionales.strip()
            if not datos_opcionales.endswith("]"):
                raise ErrorConfiguracionMapa(
                    "Las opciones de un hub deben terminar con ']'."
                )

            datos_opcionales = datos_opcionales.removesuffix("]")
            datos_opcionales = datos_opcionales.strip()
            self.validar_datos_opcionales_hub(datos_opcionales)

    def validar_datos_obligatorios_hub(
        self, partes_obligatorias: list[str], nombres_hubs: list[str]
    ) -> None:
        """Comprueba el nombre y las posiciones de un hub."""
        nombre: str
        posicion_x: str
        posicion_y: str

        if len(partes_obligatorias) != 3:
            raise ErrorConfiguracionMapa(
                "Un hub debe tener nombre, posición x y posición y."
            )

        nombre = partes_obligatorias[0]
        if "-" in nombre:
            raise ErrorConfiguracionMapa(
                "El nombre de un hub no puede contener guiones."
            )

        if nombre in nombres_hubs:
            raise ErrorConfiguracionMapa("El nombre de cada hub debe ser único.")

        posicion_x = partes_obligatorias[1]
        posicion_y = partes_obligatorias[2]
        try:
            int(posicion_x)
            int(posicion_y)
        except ValueError as error:
            raise ErrorConfiguracionMapa(
                "Las posiciones x e y de un hub deben ser números enteros."
            )

        nombres_hubs.append(nombre)

    def validar_datos_opcionales_hub(
        self, datos_opcionales: str
    ) -> None:
        """Comprueba las opciones de un hub."""
        opcion: str
        clave: str
        valor: str
        partes_datos_opcionales: list[str]
        partes_opcion: list[str]
        zonas_validas: list[str]
        claves_usadas: list[str]

        if not datos_opcionales:
            raise ErrorConfiguracionMapa(
                "El bloque de opciones de un hub no puede estar vacío."
            )

        if "[" in datos_opcionales or "]" in datos_opcionales:
            raise ErrorConfiguracionMapa(
                "El bloque de opciones de un hub tiene corchetes no válidos."
            )

        zonas_validas = ["normal", "blocked", "restricted", "priority"]
        claves_usadas = []
        partes_datos_opcionales = datos_opcionales.split()

        for opcion in partes_datos_opcionales:
            partes_opcion = opcion.split("=")
            if len(partes_opcion) != 2:
                raise ErrorConfiguracionMapa(
                    "Las opciones de un hub deben tener formato clave=valor."
                )

            clave = partes_opcion[0]
            valor = partes_opcion[1]

            if clave in claves_usadas:
                raise ErrorConfiguracionMapa(
                    "Una opción de un hub no puede repetirse."
                )

            claves_usadas.append(clave)

            if clave == "zone":
                if valor not in zonas_validas:
                    raise ErrorConfiguracionMapa("El tipo de zona no es válido.")
            elif clave == "color":
                if not valor:
                    raise ErrorConfiguracionMapa("El color no puede estar vacío.")
            elif clave == "max_drones":
                if not valor.isdigit() or int(valor) <= 0:
                    raise ErrorConfiguracionMapa(
                        "max_drones debe ser un entero positivo."
                    )
            else:
                raise ErrorConfiguracionMapa("La opción del hub no es válida.")

    def _validar_conexion(
        self,
        contenido_conexion: str,
        nombres_hubs: list[str],
        conexiones: list[tuple[str, str]],
    ) -> None:
        """Comprueba el contenido de una línea de conexión."""
        partes: list[str]
        datos_obligatorios: str
        datos_opcionales: str

        partes = contenido_conexion.split("[")
        if len(partes) > 2:
            raise ErrorConfiguracionMapa(
                "Una conexión solo puede tener un bloque de opciones."
            )

        datos_obligatorios = partes[0]
        datos_obligatorios = datos_obligatorios.strip()
        self.validar_datos_obligatorios_conexion(
            datos_obligatorios, nombres_hubs, conexiones
        )

        if len(partes) == 2:
            datos_opcionales = partes[1]
            datos_opcionales = datos_opcionales.strip()
            if not datos_opcionales.endswith("]"):
                raise ErrorConfiguracionMapa(
                    "Las opciones de una conexión deben terminar con ']'."
                )

            datos_opcionales = datos_opcionales.removesuffix("]")
            datos_opcionales = datos_opcionales.strip()
            self.validar_datos_opcionales_conexion(datos_opcionales)

    def validar_datos_obligatorios_conexion(
        self,
        datos_obligatorios: str,
        nombres_hubs: list[str],
        conexiones: list[tuple[str, str]],
    ) -> None:
        """Comprueba el formato origen-destino de una conexión."""
        partes: list[str]
        origen: str
        destino: str

        partes = datos_obligatorios.split("-")
        if len(partes) != 2:
            raise ErrorConfiguracionMapa(
                "Una conexión debe tener el formato origen-destino."
            )

        origen = partes[0]
        origen = origen.strip()
        destino = partes[1]
        destino = destino.strip()
        if not origen or not destino:
            raise ErrorConfiguracionMapa(
                "El origen y el destino de una conexión no pueden estar vacíos."
            )

        if origen == destino:
            raise ErrorConfiguracionMapa(
                "El origen y el destino de una conexión deben ser distintos."
            )

        if not nombres_hubs:
            raise ErrorConfiguracionMapa(
                "No puede haber conexiones sin hubs definidos."
            )

        if origen not in nombres_hubs or destino not in nombres_hubs:
            raise ErrorConfiguracionMapa(
                "Una conexión solo puede usar hubs definidos previamente."
            )

        if (origen, destino) in conexiones or (destino, origen) in conexiones:
            raise ErrorConfiguracionMapa("Una conexión no puede repetirse.")

        conexiones.append((origen, destino))

    def validar_datos_opcionales_conexion(
        self, datos_opcionales: str
    ) -> None:
        """Comprueba las opciones de una conexión."""
        partes: list[str]
        clave: str
        valor: str

        if not datos_opcionales:
            raise ErrorConfiguracionMapa(
                "El bloque de opciones de una conexión no puede estar vacío."
            )

        if "[" in datos_opcionales or "]" in datos_opcionales:
            raise ErrorConfiguracionMapa(
                "El bloque de opciones de una conexión tiene corchetes no válidos."
            )

        partes = datos_opcionales.split("=")
        if len(partes) != 2:
            raise ErrorConfiguracionMapa(
                "La opción de una conexión debe tener formato clave=valor."
            )

        clave = partes[0]
        valor = partes[1]
        if clave != "max_link_capacity":
            raise ErrorConfiguracionMapa(
                "La única opción de una conexión es max_link_capacity."
            )

        if not valor.isdigit() or int(valor) <= 0:
            raise ErrorConfiguracionMapa(
                "max_link_capacity debe ser un entero positivo."
            )
