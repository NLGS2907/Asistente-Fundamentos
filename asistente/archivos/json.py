"Módulo que procesa archivos en formato JSON."

from json import dump, load
from os import PathLike
from typing import TextIO, TypeAlias, Union

RutaOArchivo: TypeAlias = Union[PathLike, TextIO]
DiccionarioPares: TypeAlias = dict[str, str]


def cargar_json(archivo: RutaOArchivo) -> DiccionarioPares:
    "Lee y carga un archivo JSON."

    dic_pares_valores = {}

    if isinstance(archivo, (str, bytes, PathLike)):
        with open(archivo, mode='r', encoding="utf-8") as arch:
            dic_pares_valores = load(arch)

    else:
        dic_pares_valores = load(archivo)

    return dic_pares_valores

def guardar_json(dic_pares_valores: DiccionarioPares,
                 archivo: RutaOArchivo,
                 *,
                 sangria: int=4) -> None:
    "Recibe un diccionario y guarda la informacion del mismo en un archivo JSON."

    if isinstance(archivo, (str, bytes, PathLike)):
        with open(archivo, mode='w', encoding="utf-8") as arch:
            dump(dic_pares_valores, arch, indent=sangria)

    else:
        dump(dic_pares_valores, archivo, indent=sangria)
