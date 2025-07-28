"""
Módulo que procesa archivos de guías.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Optional, TypeAlias, Union

from ..db import existe_dato_en_tabla, sacar_datos_de_tabla
from ..logger import AssistLogger
from .general import lista_carpetas
from .json import cargar_json

if TYPE_CHECKING:
    from os import PathLike


DiccionarioEjercicio: TypeAlias = dict[str, Union[list[str], dict[str, list[str]]]]
DiccionarioUnidad: TypeAlias = dict[str, Union[str, DiccionarioEjercicio]]
DiccionarioGuia: TypeAlias = dict[str, Union[str, DiccionarioUnidad]]
DiccionarioStats: TypeAlias = dict[str, list[int]]

GUIA_PATH: "PathLike" = "guia"
"El directorio en donde están los archivos de guías."

GUIA_EXT: str = ".json"
"Extensión esperada por los archivos de guías."

GUIA_DEFAULT: str = "2024C1"
"La versión de la guía a usar por defecto o en casos de versiones inválidas."


def version_es_valida(version: str, carpeta_guias: "PathLike"=GUIA_PATH) -> bool:
    """
    Verifica que la versión especificada existe dentro del directorio de
    las guías de ejercicios.
    """

    return version in lista_carpetas(carpeta_guias)


def archivos_guia(version: str, carpeta: "PathLike") -> Optional[set["PathLike"]]:
    """
    Dado un directorio, devuelve una lista de strings con todos los nombres
    de los archivos que contienen las unidades de la guía, si y sólo si éstas
    son de la extensión utilizada para contener los enunciados.
    """

    if not version_es_valida(version):
        return None

    version_path = Path(carpeta) / version
    return set(u.name for u in version_path.iterdir()
               if (u.is_file() and
                   u.suffix == GUIA_EXT))


def cargar_guia(version: str, carpeta: "PathLike"=GUIA_PATH) -> Optional[DiccionarioGuia]:
    """
    Carga la guía de ejercicios en un diccionario de diccionarios, donde cada
    sub-diccionario tiene los pares clave valor en donde la clave es el numero
    de ejercicio y el valor el enunciado del mismo, ya formateado.

    Devuelve `None` si la versión pasada no es válida.
    """

    if not version_es_valida(version, carpeta):
        return None

    unidades = archivos_guia(version, carpeta)
    guia = {"version" : version}

    for unidad in range(1, len(unidades) + 1):
        guia[str(unidad)] = cargar_json(f"{carpeta}/{version}/guia_{unidad}{GUIA_EXT}")

    return guia


def lista_unidades(guia: DiccionarioGuia) -> list[str]:
    """
    Dada una guía, devuelve una lista de sus unidades.
    """

    copia_guia = guia.copy()
    copia_guia.pop("version") # Se escluye la clave especial 'version'

    return list(copia_guia)


def lista_ejercicios(guia: DiccionarioGuia, unidad: str) -> list[str]:
    """
    Dada una guía de ejercicios y la unidad, devuelve una
    lista con los números de ejercicios.
    """

    copia_unidad = guia[unidad].copy()
    copia_unidad.pop("titulo") # Se excluye la clave especial 'titulo'

    return list(copia_unidad)


def get_version_guia_por_sv(guild_id: int) -> str:
    "Consigue la versión de guía de un servidor en específico."

    if existe_dato_en_tabla(tabla="guias",
                            guild_id=guild_id):
        return sacar_datos_de_tabla(tabla="guias",
                                    sacar_uno=True,
                                    guild_id=guild_id)[2]

    return GUIA_DEFAULT


def get_guia_por_sv(guild_id: int, version: Optional[str]=None) -> "DiccionarioGuia":
    "Carga una guía basada en la versión de su servidor."

    version = version or get_version_guia_por_sv(guild_id)
    version_a_usar = cargar_guia(version)
    log = AssistLogger()

    if version_a_usar is None:
        formato_log = {"version": version,
                        "default_ver": GUIA_DEFAULT,
                        "guild_id": guild_id}

        log.warning("La versión '%(version)s' no fue encontrada, " % formato_log +
                            "configurando la versión predeterminada " +
                            "'%(default_ver)s' para id %(guild_id)s..." % formato_log)
        version_a_usar = cargar_guia(GUIA_DEFAULT)
        log.warning("listo.")

    return version_a_usar