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


    @classmethod
    def opciones(cls, incluir_plebeyo: bool=False) -> dict[str, int]:
        """
        Devuelve un diccionario con los contenidos de los tipos de permisos.
        """

        niveles = {nivel.name: nivel.value for nivel in cls}

        if not incluir_plebeyo:
            niveles.pop("PLEBEYO")

        return niveles


    def superior_a(self, otro: "NivelPermisos") -> bool:
        """
        Compara manualmente si un nivel de permisos es estrictamente superior a otro.
        """

        self.value < otro.value


    def inferior_a(self, otro: "NivelPermisos") -> bool:
        """
        Compara manualmente si un nivel de permisos es estrictamente inferior a otro.
        """

        self.value > otro.value
