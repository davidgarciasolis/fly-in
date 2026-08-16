"""Salida de los movimientos de la simulación."""


class Render:
    """Muestra los movimientos de una simulación."""

    def imprimir_movimientos(self, movimientos: list[list[str]]) -> None:
        """Imprime una línea por cada turno de la simulación."""
        for movimientos_turno in movimientos:
            print(" ".join(movimientos_turno))
