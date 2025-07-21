"""
Módulo para atajos de consultas de guías de ejercicios.
"""

from ..database import (actualizar_dato_de_tabla, existe_dato_en_tabla,
                        insertar_datos_en_tabla)

TABLA_GUIAS: str = "guias"
"Nombre de la tabla de guias relevante en la DB."


def actualizar_version_guia(nueva_guia: str, guild_id: int) -> bool:
    """
    Devuelve la versión de la guía de un guild específico.

    Devuelve 'True' si hay una versión presente, sino devuelve 'False'.
    """

    if existe_dato_en_tabla(tabla=TABLA_GUIAS, guild_id=guild_id):
        actualizar_dato_de_tabla(tabla=TABLA_GUIAS,
                                 nombre_col="guia",
                                 valor=nueva_guia)
        return True

    insertar_datos_en_tabla(tabla=TABLA_GUIAS,
                            llave_primaria_por_defecto=True,
                            valores=(guild_id, nueva_guia))
    return False
