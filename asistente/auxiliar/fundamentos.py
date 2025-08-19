"Módulo para funciones auxiliares del servidor de fundamentos."

from typing import TYPE_CHECKING, Optional

from ..db.atajos import insertar_padron

if TYPE_CHECKING:
      from discord import Guild, Interaction, Role

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


async def procesar_padron(padron: int, practica: Optional[str], interaccion: "Interaction") -> str:
    "Procesa el padrón que eligió el alumno, y devuelve un mensaje a mostrar."

    usuario = insertar_padron(padron, interaccion.user.id)
    if practica is None:
        practica = "" # necesitamos que sea un string sí o sí

    if usuario is not None:
        if interaccion.user.id == usuario:
            return f"{interaccion.user.mention}, vos ya estás registrado con este padrón."

        return (f"Lo siento {interaccion.user.mention}, pero el padrón `{padron}` "
                f"ya está tomado por el usuario <@{usuario}>.")

    return await asignar_roles(practica, interaccion)


async def asignar_roles(practica: str, interaccion: "Interaction") -> str:
    """
    Dado un rol que ya sabemos es válido, se asignan los roles correspondientes.

    ESTO SÓLO FUNCIONA si el rol que tiene el asistente tiene mayor jerarquía que los roles
    que trata de asignar. Esto se debe configurar del lado del servidor.

    Devuelve un mensaje para mostrar.
    """

    rol_alumno = interaccion.guild.get_role(ROL_ALUMNO)
    rol_practica = rol_por_practica(practica, interaccion.guild)

    roles_a_asignar = [rol_alumno]

    if rol_practica is None:
        los_roles = (f"el rol {rol_alumno.mention}, pero no parece que tengas una práctica "
                     "asignada todavía, así que me salté esa parte.")

    else:
        los_roles = f"los roles {rol_alumno.mention} y {rol_practica.mention}"
        roles_a_asignar.append(rol_practica)

    await interaccion.user.add_roles(
        *roles_a_asignar,
        # opciones
        reason="El usuario ingresó su padrón correctamente.",
        atomic=True
    )

    return f"¡Listo, {interaccion.user.mention}! Te asigné {los_roles}."


def rol_por_practica(practica: str, guild: "Guild") -> Optional["Role"]:
    "Devuelve un rol basado en el nombre de práctica dado."

    match practica.lower():
        case "alan":
            return guild.get_role(ROL_ALAN)
        case "barbara":
            return guild.get_role(ROL_BARBARA)
        case "grace":
            return guild.get_role(ROL_GRACE)
        case _:
            return None
