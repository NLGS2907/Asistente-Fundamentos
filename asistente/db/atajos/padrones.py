"Módulo para atajos de consultas de padrones."

from typing import Optional

from ..database import insertar_datos_en_tabla, sacar_datos_de_tabla

TABLA_PADRONES = "padrones"
"Nombre de la tabla de padrones relevante en la DB."


def insertar_padron(padron: int, user_id: int) -> Optional[int]:
    """
    Intenta insertar el par padrón-usuario en la tabla correspondiente.

    Si ya existe una entrada con el mismo padrón, se devuelve ese ID de usuario.
    Caso contrario, se inserta el padrón y se devuelve `None`.
    """

    res = sacar_datos_de_tabla(TABLA_PADRONES,
                               sacar_uno=True,
                               ignorar_excepciones=True,
                               # condiciones
                               padron=padron)

    if not res:
        insertar_datos_en_tabla(TABLA_PADRONES,
                                llave_primaria_por_defecto=False,
                                valores=(padron, user_id))
        return None

    # el user_id es siempre la segunda columna
    return res[1]
