"Módulo para atajos deconsultas de guilds/servers de Discord."

from ..database import actualizar_dato_de_tabla, existe_dato_en_tabla, insertar_datos_en_tabla
from .guias import actualizar_version_guia
from ...archivos import GUIA_DEFAULT

TABLA_GUILDS: str = "guilds"
"Nombre de la tabla de guilds relevante en la DB."


def actualizar_guild(guild_id: int, nombre_guild: str) -> bool:
    """
    Registra el guild en la DB.

    Devuelve `True` si el guild ya está presente, sino devuelve `False`.
    """

    if existe_dato_en_tabla(tabla=TABLA_GUILDS, id=guild_id):
        actualizar_dato_de_tabla(tabla=TABLA_GUILDS,
                                 nombre_col="nombre_guild",
                                 valor=nombre_guild,
                                 # condiciones,
                                 id=guild_id)
        return True

    insertar_datos_en_tabla(tabla=TABLA_GUILDS,
                            llave_primaria_por_defecto=False,
                            valores=(guild_id, nombre_guild))
    actualizar_version_guia(GUIA_DEFAULT, guild_id)
    return False
