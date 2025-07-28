"""
Módulo para consultas relacionadas a rutas.
"""

from typing import TYPE_CHECKING, Tuple

from ..database import sacar_datos_de_tabla

if TYPE_CHECKING:
    from os import PathLike

TABLA_RUTAS: str = "rutas"
"Nombre de la tabla de rutas relevante en la DB."


def get_ruta_de_db(nombre_ruta: str) -> "PathLike":
    "Consigue una ruta de la DB."

    res = sacar_datos_de_tabla(TABLA_RUTAS,
                               sacar_uno=True,
                               nombre_ruta=nombre_ruta)

    # El valor siempre será la tercera columna
    return res[2]


def get_rutas_de_db(nombre_ruta: str) -> Tuple["PathLike", ...]:
    "Consigue muchas rutas de la DB."

    res = sacar_datos_de_tabla(TABLA_RUTAS,
                               sacar_uno=False,
                               nombre_ruta=nombre_ruta)

    # Los valores siempre serán la tercera columna
    return tuple(col[2] for col in res)


def get_ruta_guia() -> "PathLike":
    "Consigue la ruta de las guías."

    return get_ruta_de_db("guia")


def get_ruta_cogs() -> "PathLike":
    "Consigue la ruta de los cogs."

    return get_ruta_de_db("cogs")


def get_ruta_palabras() -> "PathLike":
    "Consigue la ruta de las palabras de ahorcado."

    return get_ruta_de_db("palabras")