"""Punto de entrada del programa."""

import sys

from errores import ErrorConfiguracionMapa, ErrorSimulacion
from grafo import Grafo
from parser_mapa import ParserMapa
from simulador import Simulador


def main() -> int:
    """Lee el archivo indicado como primer argumento."""
    ruta_archivo: str
    configuracion: list[str]
    parser: ParserMapa
    simulador: Simulador
    usar_color: bool

    usar_color = False
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Uso: python3 fly-in.py <mapa> [--color]")
        return 1

    for opcion in sys.argv[2:]:
        if opcion == "--color":
            usar_color = True
        else:
            print("Las opciones admitidas son: --color.")
            return 1

    ruta_archivo = sys.argv[1]
    parser = ParserMapa(ruta_archivo)

    try:
        configuracion = parser.leer_configuracion()
        grafo = Grafo(configuracion)
        simulador = Simulador(grafo, usar_color)
        simulador.ejecutar()
    except ErrorConfiguracionMapa as error:
        print(error)
        return 1
    except ErrorSimulacion as error:
        print(error)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
