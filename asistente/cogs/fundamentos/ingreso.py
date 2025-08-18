"Cogs para comandos y eventos de ingreso de alumnos al servidor."

from typing import TYPE_CHECKING, Optional

from discord.app_commands import CheckFailure
from discord.app_commands import command as appcommand
from discord.ext.commands import Cog

from ...auxiliar import GUILD_FUNDAMENTOS, es_servidor_fundamentos
from ...excepciones import SessionNotSetUp
from ...interfaces.fundamentos import ModalIngreso
from ..general import CogGeneral

if TYPE_CHECKING:
    from discord import Interaction, Member
    from discord.app_commands import AppCommandError

    from ...bot import Asistente


class CogIngreso(CogGeneral):
    "Cog para comandos y eventos relacionados con el ingreso de alumnos."

    @staticmethod
    def es_guild_fundamentos(guild_id: Optional[int]) -> bool:
        "Verifica brevemente si el servidor actual es el de 'Fundamentos de Programación'."

        return guild_id is not None and guild_id == GUILD_FUNDAMENTOS


    def mensaje_error(self, interaccion: "Interaction", error: "AppCommandError"):
        "Muestra el mensaje a mostrar por el chat de Discord en caso de error en este Cog."

        # no es el servidor de fundamentos
        if not self.es_guild_fundamentos(interaccion.guild_id) and isinstance(error, CheckFailure):
            guild_fundamentos = self.bot.get_guild(GUILD_FUNDAMENTOS)
            nombre_guild = ("Fundamentos de Programación" if guild_fundamentos is None
                            else guild_fundamentos.name)
            return (f"Este comando es exclusivo para el servidor `{nombre_guild}`.\n"
                    "No está disponible en este contexto.")

        # no se inicio la sesión correctamente
        if self.bot.sesion is None and isinstance(error, SessionNotSetUp):
            return ("La sesión con el backend no parece estar correctamente configurada.\n"
                    "Este comando no estará disponible en este conexto.")


        # si todo falla, le delegamos la lógica al Cog general
        return super().mensaje_error(interaccion, error)


    async def interaction_check(self, _interaction) -> bool:
        "Checks especiales a correr antes de cada comando, aparte de los decoradores."

        # Todos los comandos en este Cog van a necesitar, en cierta medida,
        # interactuar con el Backend
        self.bot.sesion_bien_iniciada()

        return True


    @Cog.listener()
    async def on_member_join(self, member: "Member") -> None:
        "Un usuario nuevo entró al servidor de fundamentos."

        # No nos interesa otro caso que no sea el de fundamentos
        if not self.es_guild_fundamentos(member.guild.id):
            return

        dm = await member.create_dm()
        recipient = dm.recipient
        await dm.send(
            f"¡Hola, {member.display_name if recipient is None else recipient.mention}!\n\n"
            "Soy el Asistente de Fundamentos, y me encargo de automatizar algunas tareas "
            "en el servidor de Discord de la materia, ¡Bienvenido!\n\n"
            "Para empezar, recomendaría incluirte en el sistema con `/inscribirse` para "
            "que te pueda recordar."
        )


    @appcommand(name="inscribirse",
                description="[EXLUSIVO FUNDAMENTOS] Ingresa el usuario y le da los "
                            "roles correspondientes.")
    @es_servidor_fundamentos()
    async def inscribir_miembro(self, interaccion: "Interaction") -> None:
        "Envía un modal para que el alumno sea reconocido por el asistente y sea asignado un rol."

        await interaccion.response.send_modal(ModalIngreso(self.bot))


async def setup(bot: "Asistente"):
    "Agrega el cog de este módulo al Asistente."

    await bot.add_cog(CogIngreso(bot))
