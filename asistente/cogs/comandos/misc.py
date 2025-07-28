"""
Cog para comandos misceláneos o de consultas.
"""

from discord import Interaction, Permissions
from discord.app_commands import command as appcommand
from discord.utils import oauth_url

from ...bot import Asistente
from ..general import CogGeneral


class CogMisc(CogGeneral):
    """
    Cog para comandos misceláneos.
    """

    @appcommand(name="version",
                description="Muestra la versión del bot.")
    async def mostrar_version(self, interaccion: Interaction) -> None:
        """
        Muestra en el chat la versión actual del bot.
        """

        await interaccion.response.send_message(
            f"Mi versión actual es la `v{'.'.join(map(str, Asistente.version()))}`",
            ephemeral=True
        )


    @appcommand(name="invite",
                description="Muestra el link de invitación del asistente.")
    async def invitar_bot(self, interaccion: Interaction) -> None:
        """
        Manda un mensaje indicando cuál es el enlace de invitación del asistente.
        """

        link = oauth_url(self.bot.application_id,
                         permissions=Permissions(permissions=19327560768))

        await interaccion.response.send_message(f"Mi enlace de invitación es:\n\n{link}\n\n" +
                                                "*!Sino igual puedes apretar el botón " +
                                                "que hay en mi perfil!*",
                                                ephemeral=True)


async def setup(bot: "Asistente"):
    """
    Agrega el cog de este módulo al Asistente.
    """

    await bot.add_cog(CogMisc(bot))
