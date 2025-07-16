"""
Módulo que procesa archivos en format oJSON.
"""

from json import dump, load
from typing import TypeAlias, TYPE_CHECKING

if TYPE_CHECKING:
    from os import PathLike

DiccionarioPares: TypeAlias = dict[str, str]

def cargar_json(ruta_archivo: "PathLike") -> DiccionarioPares:
    """
    Lee y carga un archivo JSON.
    """

    dic_pares_valores = {}

    with open(ruta_archivo, mode='r', encoding="utf-8") as archivo:
        dic_pares_valores = load(archivo)

    return dic_pares_valores

def guardar_json(dic_pares_valores: DiccionarioPares,
                 ruta_archivo: "PathLike",
                 *,
                 sangria: int=4) -> None:
    """
    Recibe un diccionario y guarda la informacion del mismo en un archivo JSON.
    """

    with open(ruta_archivo, mode='w', encoding="utf-8") as archivo:
        dump(dic_pares_valores, archivo, indent=sangria)