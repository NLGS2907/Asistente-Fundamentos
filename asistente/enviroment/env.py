"Módulo que procesa archivos de variables de entorno."

from os import environ
from typing import TypeAlias, TYPE_CHECKING

if TYPE_CHECKING:
    from os import PathLike

EnvDict: TypeAlias = dict[str, str]
EnvResDict: TypeAlias = dict[str, bool]

ENV_EXT: str = ".env"
"Extensión esperada por el archivo de variables de entorno."


def leer_env(ruta: "PathLike"=ENV_EXT) -> EnvDict:
    "Lee un archivo y carga en un diccionario todas las variables de enorno que encuentra."
    envs = {}
    sep = "="

    with open(ruta, mode="r", encoding="utf-8") as archivo_envs:
        for linea in archivo_envs:
            linea = linea.strip()
            linea_partida = linea.split(sep)

            clave = linea_partida[0]
            valor = "".join(linea_partida[1:]) # En caso de que haya más de un '='

            # sanitizar el valor un poco
            valor = valor.strip().strip("\"").strip("'")

            envs[clave] = valor

    return envs


def cargar_envs(envs: EnvDict) -> EnvResDict:
    """
    Intenta subir todas las variables de entorno que describe el diccionario dado. No intenta
    sobreescribir las variables si estan ya se encuentran en `os.environ`.

    Devuelve otro diccionario con las mismas claves indicando el éxito individual de cada subida.
    """

    env_res = {}

    for clave, valor in envs.items():
        if clave in environ:
            env_res[clave] = False
            continue

        environ[clave] = valor
        env_res[clave] = True

    return env_res


def leer_y_cargar_envs(ruta: "PathLike"=ENV_EXT) -> None:
    "Función de conveniencia para leer y cargar variables de entorno de un archivo ENV."

    envs = leer_env(ruta)
    cargar_envs(envs)
