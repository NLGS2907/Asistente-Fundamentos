"""
Módulo para checks auxiliares.
"""

from discord import Interaction, Thread
from discord.app_commands import check as appcheck

from ..db.atajos import get_admins_por_nivel_y_guild
from ..db.enums import NivelPermisos


def _verificar_permisos(interaccion: Interaction,
                        nivel: NivelPermisos,
                        al_menos: bool) -> bool:
    if interaccion.guild is None:
            # Esto no es un guild, abortar
            return False

    candidatos_usuarios, candidatos_roles = get_admins_por_nivel_y_guild(nivel,
                                                                         interaccion.guild_id,
                                                                         por_lo_menos=al_menos)

    # a este punto el usuario está garantizado de ser tipo Member, por lo que tiene .roles
    return ((interaccion.user.id in candidatos_usuarios)
            or any(role.id in candidatos_roles for role in interaccion.user.roles))


def tiene_permisos(interaccion: Interaction) -> bool:
    """
    Verifica si el invocador del comando tiene cualquier clase de privilegios relevantes.
    """

    return _verificar_permisos(interaccion, NivelPermisos.PLEBEYO, al_menos=True)


def _permisos_check(nivel: NivelPermisos, *, al_menos: bool):
    def verificar_permisos_predicado(interaccion: Interaction) -> bool:
        """
        Verifica si el usuario que invoca el comando tiene los privilegios adecuados.

        Siempre los permisos individuales tienen prioridad por sobre los permisos de rol.
        Si alguien tiene ambos, se prefiere el nivel del permiso individual.
        """

        return _verificar_permisos(interaccion, nivel, al_menos)

    return appcheck(verificar_permisos_predicado)


def permisos_con_nivel(nivel: NivelPermisos):
    """
    Verifica si el invocador del comando tiene exactamente el nivel de privilegios dado.
    """

    return _permisos_check(nivel, al_menos=False)


def permisos_de_al_menos_nivel(nivel: NivelPermisos):
    """
    Verifica si el invocador del comando tiene al menos el nivel de privilegios dado.
    """

    return _permisos_check(nivel, al_menos=True)


def es_hilo():
    """
    Verifica si la interacción ocurrió en un hilo.
    """

    def predicado(interaccion: Interaction) -> bool:
        """
        Crea el check correspondiente.
        """

        return isinstance(interaccion.channel, Thread)

    return appcheck(predicado)