"""Errores específicos de la aplicación."""


class ErrorConfiguracionMapa(ValueError):
    """Indica que no se pudo cargar un archivo de configuración de mapa."""


class ErrorSimulacion(RuntimeError):
    """Indica que no es posible completar la simulación."""
