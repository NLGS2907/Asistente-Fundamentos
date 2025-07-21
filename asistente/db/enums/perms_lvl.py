"""
Módulo para enumerar niveles de permisos en los comandos.
"""

from enum import IntEnum


class NivelPermisos(IntEnum):
    """
    Niveles de privilegio para correr comandos.
    """

    ADMINISTRADOR = 1
    MODERADOR = 2

    # Variante especial para comparar en casos borde
    PLEBEYO = 999


    def superior_a(self, otro: "NivelPermisos") -> bool:
        """
        Compara manualmente si un nivel de permisos es superior a otro.
        """

        self.value >= otro.value
