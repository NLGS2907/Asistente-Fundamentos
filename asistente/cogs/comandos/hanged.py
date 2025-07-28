"""
Cog para comandos del ahorcado.
"""

from typing import TYPE_CHECKING, Optional

from discord import Interaction
from discord.app_commands import command as appcommand
from discord.enums import ChannelType

from ...ahorcado import Ahorcado
from ...interfaces import VistaAdivinacion
from ..general import CogGeneral

if TYPE_CHECKING:

    from ...bot import Asistente

FMT_FECHA: str = r"%Y-%m-%d_%H-%M-%S_%f"


class CogHanged(CogGeneral):
    """
    Cog para comandos relacionados al ahorcado.
    """

    @appcommand(name="ahorcado",
                description="Interactúa con un juego de ahorcado.")
    async def crear_sala(self,
                         interaccion: Interaction,
                         frase: Optional[str]=None,
                         vidas: int=7) -> None:
        """
        Dependiendo de los comandos que se pasen, interactúa con
        las de juego de ahorcado que hay actualmente.
        """

        if interaccion.channel.type != ChannelType.text:
            await interaccion.response.send_message(("*No puedo crear una partida, debe ser" +
                                                     " un canal de texto.*"),
                                                    ephemeral=True)

        await interaccion.response.send_message("¡Partida Creada!",
                                                ephemeral=True)
        mensaje_pivote = await interaccion.channel.send("¡Partida de ahorcado en juego!")
        hilo = await mensaje_pivote.create_thread(
            name=f"AHORCADO - Partida {self.bot.inicializado_en.strftime(FMT_FECHA)}",
            auto_archive_duration=60,
            reason="Alguien quiere jugar al ahorcado.")
        frase_a_usar = None

        spoilertag = "||"  # Por si el usuario la declaró con spoilertags
        frase = (' '.join(frase.replace(spoilertag, '').split())
                 if frase is not None
                 else None)

        if frase: # El usuario indicó una con la que jugar
            frase_a_usar = frase

        self.bot.partidas[str(hilo.id)] = Ahorcado(frase=frase_a_usar,
                                                   vidas_maximas=vidas,
                                                   id_mensaje_padre=mensaje_pivote.id)
        partida = self.bot.partidas[str(hilo.id)]
        await hilo.send(content=partida,
                        view=VistaAdivinacion(self.bot))


async def setup(bot: "Asistente"):
    """
    Agrega el cog de este módulo al Asistente.
    """

    await bot.add_cog(CogHanged(bot))
