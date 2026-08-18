"""Salida de los movimientos de la simulación."""

from movimiento import Movimiento


class Render:
    """Muestra los movimientos de una simulación."""

    CODIGOS_COLORES: dict[str, str] = {
        "black": "30",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magenta": "35",
        "cyan": "36",
        "white": "37",
        "gray": "90",
        "orange": "33",
        "purple": "35",
        "brown": "33",
        "lime": "92",
        "gold": "93",
        "maroon": "31",
        "darkred": "31",
        "crimson": "31",
        "violet": "35",
    }

    def __init__(self, usar_color: bool = False) -> None:
        """Indica si la salida debe incluir colores ANSI."""
        self.usar_color: bool = usar_color

    def imprimir_movimientos(self, movimientos: list[list[Movimiento]]) -> None:
        """Imprime una línea por cada turno de la simulación."""
        for movimientos_turno in movimientos:
            movimientos_ordenados = sorted(movimientos_turno)
            textos: list[str] = []

            for movimiento in movimientos_ordenados:
                texto = self.construir_movimiento(movimiento)
                textos.append(texto)

            print(" ".join(textos))

    def construir_movimiento(self, movimiento: Movimiento) -> str:
        """Construye el texto que representa un movimiento."""
        dron = movimiento.get_dron()
        hub = movimiento.get_hub()
        conexion = movimiento.get_conexion()
        identificador = dron.get_identificador()

        if hub is not None:
            texto = f"D{identificador}-{hub.nombre}"
            return self.colorear(texto, hub.color)

        if conexion is not None:
            origen = conexion.origen.nombre
            destino = conexion.destino.nombre
            return f"D{identificador}-{origen}-{destino}"

        return ""

    def colorear(self, texto: str, color: str | None) -> str:
        """Devuelve el texto con color ANSI cuando está activado."""
        if not self.usar_color or color is None:
            return texto

        codigo = self.CODIGOS_COLORES.get(color.lower())
        if codigo is None:
            return texto

        return f"\033[{codigo}m{texto}\033[0m"
