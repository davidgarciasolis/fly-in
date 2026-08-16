"""Punto de entrada del programa."""

import sys

from errores import ErrorConfiguracionMapa
from grafo import Grafo
from parser_mapa import ParserMapa
from render import Render
from simulador import Simulador


def main() -> int:
    """Lee el archivo indicado como primer argumento."""
    ruta_archivo: str
    linea: str
    configuracion: list[str]
    parser: ParserMapa
    simulador: Simulador
    render: Render
    movimientos: list[list[str]]

    ruta_archivo = sys.argv[1]
    parser = ParserMapa(ruta_archivo)

    try:
        configuracion = parser.leer_configuracion()
        grafo = Grafo(configuracion)
        simulador = Simulador(grafo)
        movimientos = simulador.ejecutar()
        render = Render()
        render.imprimir_movimientos(movimientos)
    except ErrorConfiguracionMapa as error:
        print(error)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
