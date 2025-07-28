"""
Cog para comandos que requieren permisos especiales.
"""

from os import execl
from sys import executable as sys_executable
from typing import TYPE_CHECKING

from discord import Interaction
from discord.app_commands import Choice, choices, describe
from discord.app_commands import command as appcommand

from ...auxiliar import permisos_de_al_menos_nivel
from ...db.enums import NivelPermisos
from ...logger import LOG_PATH
from ..general import CogGeneral

if TYPE_CHECKING:
    from ...bot import Asistente


class CogAdmin(CogGeneral):
    """
    Cog de comandos generales que requieren permisos.
    """

    @appcommand(name="clear",
                description="[MOD] Limpia el canal de mensajes del bot.")
    @describe(limite="Cuántos mensajes inspeccionar para borrar")
    @choices(completo=[
        Choice(name="Sí", value=1),
        Choice(name="No", value=0)
    ])
    @permisos_de_al_menos_nivel(NivelPermisos.MODERADOR)
    async def limpiar_mensajes(self,
                               interaccion: Interaction,
                               limite: int,
                               completo: Choice[int]=1) -> None:
        """
        Limpia los mensajes del bot del canal de donde se
        invoca el comando.

        Si 'completo' es seleccionado, también borra los
        mensajes de los usuarios que invocan los comandos.
        """

        eliminados = await interaccion.channel.purge(limit=limite + 1,
                                                     check=self.bot.es_mensaje_de_bot)

        mensaje = (f"`{len(eliminados)}` mensaje/s fueron eliminados de " +
                   f"{interaccion.channel.name} en {interaccion.guild.name}")


        await interaccion.response.send_message(content=mensaje,
                                                ephemeral=True)
        self.bot.log.info(mensaje)


    @appcommand(name="shutdown",
                description="[ADMIN] Apaga el bot.")
    @permisos_de_al_menos_nivel(NivelPermisos.ADMINISTRADOR)
    async def shutdown(self, interaccion: Interaction) -> None:
        """
        Apaga el bot y lo desconecta.
        """

        await interaccion.response.send_message(content="Apagando el asistente...",
                                                ephemeral=True)
        self.bot.log.info(f"Cerrando bot {str(self.bot.user)}...")

        await self.bot.close()


    @appcommand(name="reboot",
                description="[ADMIN] Reinicia el bot.")
    @permisos_de_al_menos_nivel(NivelPermisos.ADMINISTRADOR)
    async def reboot(self, interaccion: Interaction) -> None:
        """
        Reinicia el bot, apagándolo y volviéndolo a conectar.
        """

        if not sys_executable:

            mensaje = "[ERROR] No se pudo reiniciar el asistente."

            await interaccion.response.send_message(content=mensaje,
                                                    ephemeral=True)
            self.bot.log.error(mensaje)
            return

        mensaje = f"Reiniciando bot **{str(self.bot.user)}...**"

        await interaccion.response.send_message(content=mensaje,
                                                ephemeral=True)
        self.bot.log.info(mensaje)

        execl(sys_executable, sys_executable, "-m", "asistente")


    @appcommand(name="flush",
                description="[MOD] Vacía el archivo de registro.")
    @permisos_de_al_menos_nivel(NivelPermisos.MODERADOR)
    async def logflush(self, interaccion: Interaction):
        """
        Vacía el contenido del archivo de registro.
        """

        with open(LOG_PATH, mode='w', encoding="utf-8"):
            await interaccion.response.send_message("**[AVISO]** Vaciando archivo en " +
                                                    f"`{LOG_PATH}`...",
                                                    ephemeral=True)


    @appcommand(name="uptime",
                description="[MOD] Calcula el tiempo que el bot estuvo activo.")
    @permisos_de_al_menos_nivel(NivelPermisos.MODERADOR)
    async def calcular_uptime(self, interaccion: Interaction) -> None:
        """
        Calcula el tiempo que el bot estuvo corriendo.
        """

        delta = self.bot.uptime

        dias = (f"`{delta.days}` día/s" if delta.days > 9 else "")

        horas_posibles = (delta.seconds // 3600)
        horas = (f"`{horas_posibles}` hora/s" if horas_posibles > 0 else "")

        minutos_posibles = ((delta.seconds % 3600) // 60)
        minutos = (f"`{minutos_posibles}` minuto/s" if minutos_posibles > 0 else "")

        segundos_posibles = (delta.seconds % 60)
        segundos = (f"`{segundos_posibles}` segundo/s" if segundos_posibles > 0 else "")

        tiempo = [tmp for tmp in [dias, horas, minutos, segundos] if tmp]
        if len(tiempo) > 1:
            ultimo = tiempo.pop()
            tiempo[-1] = f"{tiempo[-1]} y {ultimo}"


        await interaccion.response.send_message(f"***{self.bot.user}** estuvo activo por " +
                                                f"{', '.join(tiempo)}.*",
                                                ephemeral=True)


async def setup(bot: "Asistente"):
    """
    Agrega el cog de este módulo al Asistente.
    """

    await bot.add_cog(CogAdmin(bot))
