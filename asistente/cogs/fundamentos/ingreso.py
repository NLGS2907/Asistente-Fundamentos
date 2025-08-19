"Cogs para comandos y eventos de ingreso de alumnos al servidor."

from typing import TYPE_CHECKING

from discord.app_commands import CheckFailure
from discord.app_commands import command as appcommand
from discord.ext.commands import Cog

from ...auxiliar import GUILD_FUNDAMENTOS, es_guild_fundamentos, es_servidor_fundamentos
from ...interfaces.fundamentos import ModalIngreso
from ..con_sesion import CogHTTP

if TYPE_CHECKING:
    from discord import Interaction, Member
    from discord.app_commands import AppCommandError

    from ...bot import Asistente


class CogIngreso(CogHTTP):
    "Cog para comandos y eventos relacionados con el ingreso de alumnos."

    def mensaje_error(self, interaccion: "Interaction", error: "AppCommandError"):
        "Muestra el mensaje a mostrar por el chat de Discord en caso de error en este Cog."

        # no es el servidor de fundamentos
        if not es_guild_fundamentos(interaccion.guild_id) and isinstance(error, CheckFailure):
            guild_fundamentos = self.bot.get_guild(GUILD_FUNDAMENTOS)
            nombre_guild = ("Fundamentos de Programación" if guild_fundamentos is None
                            else guild_fundamentos.name)
            return (f"Este comando es exclusivo para el servidor `{nombre_guild}`.\n"
                    "No está disponible en este contexto.")

        return super().mensaje_error(interaccion, error)


    @Cog.listener()
    async def on_member_join(self, member: "Member") -> None:
        "Un usuario nuevo entró al servidor de fundamentos."

        # No nos interesa otro caso que no sea el de fundamentos
        if not self.es_guild_fundamentos(member.guild.id):
            return

        # dm = await member.create_dm()
        # recipient = dm.recipient
        # await dm.send(
        #     f"¡Hola, {member.display_name if recipient is None else recipient.mention}!\n\n"
        #     "Soy el Asistente de Fundamentos, y me encargo de automatizar algunas tareas "
        #     "en el servidor de Discord de la materia, ¡Bienvenido!\n\n"
        #     "Para empezar, recomendaría incluirte en el sistema con `/inscribirse` para "
        #     "que te pueda recordar."
        # )


    @appcommand(name="roles",
                description="[EXLUSIVO FUNDAMENTOS] Ingresa el padrón para poder recibir los "
                            "roles de alumno y de las prácticas.")
    @es_servidor_fundamentos()
    async def inscribir_miembro(self, interaccion: "Interaction") -> None:
        "Envía un modal para que el alumno sea reconocido por el asistente y sea asignado un rol."

        await interaccion.response.send_modal(ModalIngreso(self.bot))


async def setup(bot: "Asistente"):
    "Agrega el cog de este módulo al Asistente."

    await bot.add_cog(CogIngreso(bot))
