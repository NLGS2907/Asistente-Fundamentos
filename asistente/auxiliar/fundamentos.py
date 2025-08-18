"Módulo para funciones auxiliares del servidor de fundamentos."

from typing import TYPE_CHECKING

from ..db.atajos import insertar_padron

if TYPE_CHECKING:
      from discord import Interaction

# -- Códigos de error 400 --
MISSING_PADRON: str = "MISSING_PADRON"
INVALID_PADRON: str = "INVALID_PADRON"
# -- Códigos de error 500 --
NO_CURRENT_CUATRI: str = "NO_CURRENT_CUATRI"
INERNAL_SERVER_ERROR: str = "INERNAL_SERVER_ERROR"

# IDs de roles relevantes
ROL_ALUMNO: int = 653342053018632192
ROL_ALAN: int = 653342149349474334
ROL_BARBARA: int = 653342150683263005
ROL_GRACE: int = 653342153245982730
ROL_ALUMNI: int = 759091780644765713


async def procesar_padron(padron: int, interaccion: "Interaction") -> str:
    "Procesa el padrón que eligió el alumno, y devuelve un mensaje a mostrar."

    usuario = insertar_padron(padron, interaccion.user.id)

    if usuario is not None:
        if interaccion.user.id == usuario:
            return f"{interaccion.user.mention}, vos ya estás registrado con este padrón."

        return (f"Lo siento {interaccion.user.mention}, pero el padrón `{padron}` "
                f"ya está tomado por el usuario <@{usuario}>.")

    return await asignar_roles(interaccion)


async def asignar_roles(interaccion: "Interaction") -> str:
    """
    Dado un rol que ya sabemos es válido, se asignan los roles correspondientes.

    ESTO SÓLO FUNCIONA si el rol que tiene el asistente tiene mayor jerarquía que los roles
    que trata de asignar. Esto se debe configurar del lado del servidor.

    Devuelve un mensaje para mostrar.
    """

    rol_alumno = interaccion.guild.get_role(ROL_ALUMNO)

    await interaccion.user.add_roles(
        rol_alumno,
        # opciones
        reason="El usuario ingresó su padrón correctamente.",
        atomic=True
    )

    return f"¡Listo, {interaccion.user.mention}! Te asigné los roles {rol_alumno.mention}."
