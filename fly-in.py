"""Punto de entrada del programa."""

import sys

from errores import ErrorConfiguracionMapa, ErrorSimulacion
from grafo import Grafo
from parser_mapa import ParserMapa
from render import Render
from simulador import Simulador
from movimiento import Movimiento


def main() -> int:
    """Lee el archivo indicado como primer argumento."""
    ruta_archivo: str
    configuracion: list[str]
    parser: ParserMapa
    simulador: Simulador
    render: Render
    movimientos: list[list[Movimiento]]
    usar_color: bool

    usar_color = False
    if len(sys.argv) == 3:
        if sys.argv[2] != "--color":
            print("Las opciones admitidas son: --color.")
            return 1
        usar_color = True
    elif len(sys.argv) != 2:
        print("Uso: python3 fly-in.py <mapa> [--color]")
        return 1

    ruta_archivo = sys.argv[1]
    parser = ParserMapa(ruta_archivo)

    try:
        configuracion = parser.leer_configuracion()
        grafo = Grafo(configuracion)
        simulador = Simulador(grafo)
        movimientos = simulador.ejecutar()
    except ErrorConfiguracionMapa as error:
        print(error)
        return 1
    except ErrorSimulacion as error:
        print(error)
        return 1

    render = Render(usar_color)
    render.imprimir_movimientos(movimientos)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
