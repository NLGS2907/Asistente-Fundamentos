"""
Módulo para atajos de consultas de propiedades globales.
"""

from typing import TYPE_CHECKING

from ..database import sacar_datos_de_tabla

if TYPE_CHECKING:
    from ..database import FetchResult

TABLA_PROPIEDADES: str = "propiedades"
"Nombre de la tabla de propiedades relevante en la DB."


def get_propiedad(propiedad: str) -> "FetchResult":
    "Consigue alguna propiedad del asistente."

    return sacar_datos_de_tabla(TABLA_PROPIEDADES,
                                sacar_uno=True,
                                nombre=propiedad)[2]
