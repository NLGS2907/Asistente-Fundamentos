"Cog para comandos misceláneos o de consultas."

from typing import TYPE_CHECKING

from discord import Colour, Interaction
from discord.app_commands import command as appcommand
from discord.utils import oauth_url

from ...embebido import Embebido
from ..general import CogGeneral

if TYPE_CHECKING:
    from ...bot import Asistente


class CogMisc(CogGeneral):
    "Cog para comandos misceláneos."

    @appcommand(name="info",
                description="Muestra información sobre el asistente.")
    async def about(self, interaccion: Interaction) -> None:
        """
        Muestra un embebido con información miscelánea del bot.
        """

        invite_link = oauth_url(client_id=self.bot.application_id,
                                permissions=self.bot.permisos_preferidos())

        embebido = Embebido(opciones=dict(
            titulo=["Información sobre el Asistente de Fundamentos"],
            color=Colour.random(),
            campos=dict(
                Propiedades=[
                    f"* **Versión:** `v{'.'.join(map(str, self.bot.version()))}`"
                ],
                Links=[
                    f"* [**Enlace de Invitación**]({invite_link})",
                    "* [**Repositorio de GitHub**]" # <- NO poner coma, está a propósito así
                    "(https://github.com/NLGS2907/Asistente-Fundamentos)"
                ]
            )
        ))

        await interaccion.response.send_message(embed=embebido, ephemeral=True)


async def setup(bot: "Asistente"):
    "Agrega el cog de este módulo al Asistente."

    await bot.add_cog(CogMisc(bot))
