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


def get_version() -> str:
    "Consigue la versión del asistente."

    return get_propiedad("version")


def get_asist_id() -> int:
    "Consigue el ID del asistente."

    return int(get_propiedad("asist_id"))


def get_sv_algo1_id() -> int:
    "Consigue el ID del servidor de 'Algoritmos y Programación 1 - Essaya'"

    return int(get_propiedad("sv_algo1_id"))


def get_rol_diego_id() -> int:
    "Consigue el ID del rol de Diego."

    return int(get_propiedad("rol_diego_id"))


def get_rol_docente_id() -> int:
    "Consigue el ID del rol de docente."

    return int(get_propiedad("rol_docente_id"))


def get_guia_default() -> str:
    "Consigue la versión predeterminada de la guía."

    return get_propiedad("guia_default")


def get_fmt_fecha() -> str:
    "Consigue el formato de fecha personalizado para el asistente."

    return get_propiedad("fmt_fecha")
