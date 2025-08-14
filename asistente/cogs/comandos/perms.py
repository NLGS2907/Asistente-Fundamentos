"Cog que agrupa comandos de permisos."

from typing import TYPE_CHECKING

from discord import Colour, Interaction, Member, Role
from discord.app_commands import Choice, choices, describe
from discord.app_commands import command as appcommand
from discord.app_commands.errors import AppCommandError, CheckFailure

from ...auxiliar.checks import permisos_de_al_menos_nivel
from ...db.atajos import (
    deop_rol,
    deop_usuario,
    get_admins_por_guild,
    get_nivel_de_admin,
    op_rol,
    op_usuario,
)
from ...db.enums import NivelPermisos
from ...embebido import Embebido
from ..general import CogGeneral, GrupoGeneral

if TYPE_CHECKING:
    from ...bot import Asistente
    from ..general import GroupsList


class GrupoPermsOp(GrupoGeneral):
    "Grupo para comandos que añaden o manejan permisos."

    def __init__(self, bot: "Asistente") -> None:
        "Inicializa una instancia de este grupo."

        super().__init__(bot,
                         name="op",
                         description="Comandos para añadir/manejar permisos de usuarios o roles.")


    async def interaction_check(self, interaction: Interaction) -> bool:
        """
        Verifica si el usuario tiene los permisos necesarios para ejecutar comandos
        en este grupo.
        """

        # Por ahora preferimos manejar cada caso individualmente
        return True


    async def on_error(self, interaccion: Interaction, error: AppCommandError) -> None:
        "Avisa el usuario que un comando falló."

        if isinstance(error, CheckFailure):
            mensaje = f"{interaccion.user.mention}, no tenés permisos para ejecutar este comando."
            await interaccion.response.send_message(content=mensaje,
                                                    ephemeral=True)
            return

        raise error from error


    @appcommand(name="usuario",
                description="[MOD] Añade nuevos permisos para un usuario en este guild.")
    @describe(usuario="El usuario al que modificarle los permisos.",
              nivel="El nivel de permisos. Cuanto menor el número, más privilegiado el nivel.")
    @choices(nivel=[Choice(name=f"{nombre} ({valor})", value=valor)
                    for nombre, valor in NivelPermisos.opciones().items()])
    @permisos_de_al_menos_nivel(NivelPermisos.MODERADOR)
    async def perms_usuario(self,
                            interaccion: Interaction,
                            usuario: Member,
                            nivel: Choice[int]) -> None:
        "Proporciona permisos a un usuario dado."

        if usuario.bot:
            await interaccion.response.send_message(
                content=f"No se puede dar permisos al usuario {usuario.mention}"
                         " porque se ha detectado que es un bot o una app.",
                ephemeral=True)
            return

        if interaccion.guild_id is None:
            await interaccion.response.send_message(
                content="No se pudo completar la operación porque no se puede detectar el ID del"
                        " servidor actual. ¿Estás seguro de que estamos es un servidor?",
                ephemeral=True)
            return

        nivel_permisos = get_nivel_de_admin(interaccion.user.id,
                                            [rol.id for rol in interaccion.user.roles],
                                            interaccion.guild_id)

        if (nivel_permisos is not None # no puede ser None igual porque sino el check no pasaría
            and nivel_permisos.inferior_a(NivelPermisos(nivel.value))):
            await interaccion.response.send_message(
                content=f"{interaccion.user.mention}, vos no tenés los permisos necesarios para"
                        f" elevar a alguien al nivel `{nivel.value}`; tenés permisos de nivel"
                        f" `{nivel_permisos}`.",
                ephemeral=True)
            return

        if usuario.id == interaccion.guild.owner_id:
            await interaccion.response.send_message(
                # Sin esto, todavía es posible que un Admin con el mismo nivel que el owner
                # le saque los permisos. Por diseño eso no se permite.
                content="Los permisos del dueño del servidor no se tocan.",
                ephemeral=True)
            return

        viejo_nivel = op_usuario(usuario.id, NivelPermisos(nivel.value), interaccion.guild_id)
        if viejo_nivel is None:
            msg = (f"Se agregó a {usuario.mention} al registro de permisos con "
                   f"nivel `{nivel.value}`.")
            log_msg = (f"Se agregó a {usuario.global_name} al registro de permisos del guild "
                       f" '{interaccion.guild.name}' con nivel {nivel.name} ({nivel.value}).")
        else:
            msg = (f"Se actualizaron los permisos de {usuario.mention} de"
                   f" `{viejo_nivel}` a `{nivel.value}`.")
            log_msg = (f"Se actualizaron los permisos de {usuario.global_name} en el guild "
                       f" '{interaccion.guild.name}' de {viejo_nivel.name} ({viejo_nivel.value})"
                       f" a {nivel.name} ({nivel.value}).")

        self.bot.log.debug(log_msg)
        await interaccion.response.send_message(content=msg, ephemeral=True)


    @appcommand(name="rol",
                description="[MOD] Añade nuevos permisos para un rol en este guild.")
    @describe(rol="El rol al que modificarle los permisos.",
              nivel="El nivel de permisos. Cuanto menor el número, más privilegiado el nivel.")
    @choices(nivel=[Choice(name=f"{nombre} ({valor})", value=valor)
                    for nombre, valor in NivelPermisos.opciones().items()])
    @permisos_de_al_menos_nivel(NivelPermisos.MODERADOR)
    async def perms_rol(self,
                        interaccion: Interaction,
                        rol: Role,
                        nivel: Choice[int]) -> None:
        "Proporciona permisos a un rol de Discord dado."

        if interaccion.guild_id is None:
            await interaccion.response.send_message(
                content="No se pudo completar la operación porque no se puede detectar el ID del"
                        " servidor actual. ¿Estás seguro de que estamos es un servidor?",
                ephemeral=True)
            return

        nivel_permisos = get_nivel_de_admin(interaccion.user.id,
                                            [rol.id for rol in interaccion.user.roles],
                                            interaccion.guild_id)

        if (nivel_permisos is not None and nivel_permisos.inferior_a(NivelPermisos(nivel.value))):
            await interaccion.response.send_message(
                content=f"{interaccion.user.mention}, vos no tenés los permisos necesarios para"
                        f" elevar este rol al nivel `{nivel.value}`; tenés permisos de nivel"
                        f" `{nivel_permisos}`.",
                ephemeral=True)
            return

        viejo_nivel = op_rol(rol.id, NivelPermisos(nivel.value), interaccion.guild_id)
        if viejo_nivel is None:
            msg = (f"Se agregó el rol {rol.mention} al registro de permisos con "
                   f"nivel `{nivel.value}`.")
            log_msg = (f"Se agregó el rol {rol.name} al registro de permisos del guild "
                       f" '{interaccion.guild.name}' con nivel {nivel.name} ({nivel.value}).")
        else:
            msg = (f"Se actualizaron los permisos de {rol.mention} de"
                   f" `{viejo_nivel}` a `{nivel.value}`.")
            log_msg = (f"Se actualizaron los permisos de {rol.name} de en el guild "
                       f" '{interaccion.guild.name}' {viejo_nivel.name} ({viejo_nivel})"
                       f" a {nivel.name} ({nivel.value}).")

        self.bot.log.debug(log_msg)
        await interaccion.response.send_message(content=msg, ephemeral=True)


    @appcommand(name="list",
                description=("Devuelve una lista de todos los usuarios (y roles) que tienen"
                             " un nivel de permisos en este servidor."))
    @permisos_de_al_menos_nivel(NivelPermisos.MODERADOR)
    async def perms_list(self, interaccion: Interaction) -> None:
        "Crea una lista de permisos y la envía en forma de embebido."

        if interaccion.guild_id is None:
            await interaccion.response.send_message(
                content="No se pudo completar la operación porque no se puede detectar el ID del"
                        " servidor actual. ¿Estás seguro de que estamos es un servidor?",
                ephemeral=True)
            return

        perms_usuarios, perms_roles = get_admins_por_guild(interaccion.guild_id)
        perms_usuarios = {clave: NivelPermisos(valor) for clave, valor in perms_usuarios.items()}
        perms_roles = {clave: NivelPermisos(valor) for clave, valor in perms_roles.items()}

        perms_owner = perms_usuarios.pop(interaccion.guild.owner.id, None)
        owner_str = ("" if perms_owner is None else f" - **{perms_owner.name}**"
                     f" (`{perms_owner.value}`)")

        embebido = Embebido(opciones=dict(
            titulo=[f"Permisos del guild **{interaccion.guild.name}**"],
            descripcion=[f"Owner: {interaccion.guild.owner.mention}{owner_str}"],
            # No me podía decidir, que lo decida el destino
            color=Colour.random(),
            campos=dict(
                Usuarios=(["* _N/A_"] if not perms_usuarios else [
                    # mención manual
                    f"* <@{id_usuario}> - **{perms_usuario.name}** (`{perms_usuario.value}`)"
                    for id_usuario, perms_usuario in perms_usuarios.items()
                ]),
                Roles=(["* _N/A_"] if not perms_roles else [
                    f"* <@&{id_rol}> - **{perms_rol.name}** (`{perms_rol.value}`)"
                    for id_rol, perms_rol in perms_roles.items()
                ])
            )
        ))

        await interaccion.response.send_message(embed=embebido, ephemeral=True)


class GrupoPermsDeOp(GrupoGeneral):
    "Grupo para comandos que quitan permisos."

    def __init__(self, bot: "Asistente") -> None:
        "Inicializa una instancia de este grupo."

        super().__init__(bot,
                         name="deop",
                         description="Comandos para quitar permisos de usuarios o roles.")


    async def interaction_check(self, interaction: Interaction) -> bool:
        """
        Verifica si el usuario tiene los permisos necesarios para ejecutar comandos
        en este grupo.
        """

        return True


    async def on_error(self, interaccion: Interaction, error: AppCommandError) -> None:
        "Avisa el usuario que un comando falló."

        if isinstance(error, CheckFailure):
            mensaje = f"{interaccion.user.mention}, no tenés permisos para ejecutar este comando."
            await interaccion.response.send_message(content=mensaje,
                                                    ephemeral=True)
            return

        raise error from error


    @appcommand(name="usuario",
                description="[MOD] Quita permisos de un usuario.")
    @describe(usuario="El usuario al que sacarle los permisos.")
    @permisos_de_al_menos_nivel(NivelPermisos.MODERADOR)
    async def deperms_usuario(self,
                              interaccion: Interaction,
                              usuario: Member) -> None:
        "Intenta quitarle permisos a un usuario dado."

        if interaccion.guild_id is None:
            await interaccion.response.send_message(
                content="No se pudo completar la operación porque no se puede detectar el ID del"
                        " servidor actual. ¿Estás seguro de que estamos es un servidor?",
                ephemeral=True)
            return

        nivel_invocador = get_nivel_de_admin(interaccion.user.id,
                                             [rol.id for rol in interaccion.user.roles],
                                             interaccion.guild_id)
        nivel_objetivo = get_nivel_de_admin(usuario.id,
                                            [rol.id for rol in usuario.roles],
                                            interaccion.guild_id,
                                            ignorar_roles=True)

        if (nivel_invocador is not None and nivel_objetivo is not None
            and nivel_invocador.inferior_a(nivel_objetivo)):
            await interaccion.response.send_message(
                content=f"{interaccion.user.mention}, vos tenés permisos de nivel "
                        f"`{nivel_invocador}`, que no es suficiente para sacarle permisos"
                        f" a {usuario.mention}, que tiene permisos de nivel"
                        f" `{nivel_objetivo}`.",
                ephemeral=True)
            return

        if usuario.id == interaccion.guild.owner_id:
            await interaccion.response.send_message(
                content="Al dueño del servidor no se le puede sacar los permisos.",
                ephemeral=True)
            return

        viejo_nivel = deop_usuario(usuario.id, interaccion.guild_id)
        if viejo_nivel is None:
            msg = f"El usuario {usuario.mention} no tenía permisos."
        else:
            msg = (f"Se borraron los permisos de {usuario.mention}, que tenía"
                   f" un nivel de `{viejo_nivel}`.")
            self.bot.log.debug(f"Se borraron los permisos del usuario {usuario.global_name} en"
                               f" el guild '{interaccion.guild.name}', en donde tenía un nivel"
                               f" de {viejo_nivel.name} ({viejo_nivel}).")


        await interaccion.response.send_message(content=msg, ephemeral=True)


    @appcommand(name="rol",
                description="[MOD] Quita permisos de un rol.")
    @describe(rol="El rol al que sacarle los permisos.")
    @permisos_de_al_menos_nivel(NivelPermisos.MODERADOR)
    async def deperms_rol(self,
                          interaccion: Interaction,
                          rol: Role) -> None:
        "Intenta quitarle permisos a un rol dado."

        if interaccion.guild_id is None:
            await interaccion.response.send_message(
                content="No se pudo completar la operación porque no se puede detectar el ID del"
                        " servidor actual. ¿Estás seguro de que estamos es un servidor?",
                ephemeral=True)
            return

        nivel_invocador = get_nivel_de_admin(interaccion.user.id,
                                             [rol.id for rol in interaccion.user.roles],
                                             interaccion.guild_id)
        nivel_rol = get_admins_por_guild(interaccion.guild_id)[1].get(rol.id, None)
        if nivel_rol is not None:
            nivel_rol = NivelPermisos(nivel_rol)

        if (nivel_invocador is not None and nivel_rol is not None
            and nivel_invocador.inferior_a(nivel_rol)):
            await interaccion.response.send_message(
                content=f"{interaccion.user.mention}, vos tenés permisos de nivel "
                        f"`{nivel_invocador}`, que no es suficiente para sacarle permisos"
                        f" al rol {rol.mention}, que tiene permisos de nivel"
                        f" `{nivel_rol}`.",
                ephemeral=True)
            return

        viejo_nivel = deop_rol(rol.id, interaccion.guild_id)
        if viejo_nivel is None:
            msg = f"El rol {rol.mention} no tenía permisos."
        else:
            msg = (f"Se borraron los permisos de {rol.mention}, que tenía un"
                   f" nivel de `{viejo_nivel}`.")
            self.bot.log.debug(f"Se borraron los permisos del rol {rol.name} en el guild"
                               f" '{interaccion.guild.name}', en donde tenía un nivel"
                               f" de {viejo_nivel.name} ({viejo_nivel}).")

        await interaccion.response.send_message(content=msg, ephemeral=True)


class CogPerms(CogGeneral):
    "Cog para permisos de comandos."

    @classmethod
    def grupos(cls) -> "GroupsList":
        "Devuelve la lista de grupos asociados a este Cog."

        return [GrupoPermsOp, GrupoPermsDeOp]


async def setup(bot: "Asistente"):
    "Agrega el cog de este módulo al Asistente."

    await bot.add_cog(CogPerms(bot))
