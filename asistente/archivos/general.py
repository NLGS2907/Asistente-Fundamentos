"""
Módulo que procesa archivos en general.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from os import PathLike


def lista_carpetas(carpeta: "PathLike") -> list["PathLike"]:
    """
    Devuelve una lista de todas las carpetas que se encuentran en un
    directorio dado.
    """

    path = Path(carpeta)
    return [p.name for p in path.iterdir() if p.is_dir()]


def lista_archivos(ruta: "PathLike",
                   ext: Optional[str]=None,
                   ignorar_nombres: tuple[str, ...]=()) -> list["PathLike"]:
    """
    Busca en la ruta especificada si hay archivos, y devuelve una lista
    con los nombres de los que encuentre.

    Si `ext` no es `None`, entonces probará buscando archivos con esa extensión.
    `ext` NO debe tener un punto (`.`) adelante, es decir que `"py"` será automáticamente
    tratado como `.py`.
    """

    path = Path(ruta)
    return [file.name
            for file in path.iterdir()
            if (file.is_file() and
                ((file.suffix == f".{ext}") if ext else True) and
                all(file.stem != nombre for nombre in ignorar_nombres))
            ]


def buscar_rutas(patron: str="*",
                 nombre_ruta: Optional["PathLike"]=None,
                 recursivo: bool=True,
                 incluye_archivos: bool=True,
                 incluye_carpetas: bool=True,
                 ignorar_patrones: tuple[str, ...]=()) -> list["PathLike"]:
    """
    Busca recursivamente en todas las subrutas por los archivos
    que coincidan con el patrón dado.
    Si `ruta` no está definida se usa el directorio actual.
    """

    ruta = Path(nombre_ruta if nombre_ruta is not None else ".")

    return list(fpath.as_posix() for fpath in (ruta.rglob(patron)
                                               if recursivo
                                               else ruta.glob(patron))
                if ((fpath.is_file() if incluye_archivos else False
                    or fpath.is_dir() if incluye_carpetas else False)
                    and all(not fpath.match(patr) for patr in ignorar_patrones)))


def buscar_archivos(patron: str="*",
                    nombre_ruta: Optional["PathLike"]=None,
                    recursivo: bool=True,
                    ignorar_patrones: tuple[str, ...]=()) -> list["PathLike"]:
    """
    Busca recursivamente en todas las subrutas por las rutas
    que coincidan con el patrón dado.
    Si `ruta` no está definida se usa el directorio actual.
    """

    return buscar_rutas(patron=patron,
                        nombre_ruta=nombre_ruta,
                        recursivo=recursivo,
                        incluye_archivos=True,
                        incluye_carpetas=False,
                        ignorar_patrones=ignorar_patrones)


def buscar_carpetas(patron: str="*",
                    nombre_ruta: Optional["PathLike"]=None,
                    recursivo: bool=True,
                    ignorar_patrones: tuple[str, ...]=()) -> list["PathLike"]:
    """
    Busca recursivamente en todas las subrutas por las carpetas
    que coincidan con el patrón dado.
    Si `ruta` no está definida se usa el directorio actual.
    """

    return buscar_rutas(patron=patron,
                        nombre_ruta=nombre_ruta,
                        recursivo=recursivo,
                        incluye_archivos=False,
                        incluye_carpetas=True,
                        ignorar_patrones=ignorar_patrones)
