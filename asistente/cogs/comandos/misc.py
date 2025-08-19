"Cog para comandos misceláneos o de consultas."

from io import StringIO
from typing import TYPE_CHECKING

from discord import Colour, File
from discord.app_commands import command as appcommand
from discord.app_commands import describe
from discord.utils import oauth_url

from ...archivos import tail
from ...auxiliar import es_owner, permisos_de_al_menos_nivel
from ...db.enums import NivelPermisos
from ...embebido import Embebido
from ...logger import LOG_PATH
from ..general import CogGeneral, GrupoGeneral

if TYPE_CHECKING:
    from discord import Interaction

    from ...bot import Asistente
    from ..general import GroupsList

DISCORD_MAX_CHARS: int = 2000
"La cantidad máxima de caracteres que un mensaje de Discord puede tener."


class GrupoLog(GrupoGeneral):
    "Grupo para comandos de log."

    def __init__(self, bot: "Asistente") -> None:
        "Inicializa una instancia de este grupo."

        super().__init__(bot,
                         name="log",
                         description="Comandos para consultar/modificar el archivo de log.")


    @staticmethod
    def _menos_de_n_caracteres(cadena: str, max_chars: int) -> bool:
        """
        Detecta si un string tiene `max_chars` caracteres o más.

        Se prefiere esto a `len()` debido a su uso en strings potencialmente enormes.
        """

        count = 0
        for _ in cadena:
            count += 1
            if count >= max_chars:
                return False

        return True


    @appcommand(name="get",
                description="[MOD] Devuelve el archivo de log.")
    @permisos_de_al_menos_nivel(NivelPermisos.MODERADOR)
    async def log_get(self, interaccion: "Interaction") -> None:
        "Envía el archivo de log entero."

        await interaccion.response.send_message(file=File(LOG_PATH,
                                                          filename=LOG_PATH.lstrip("./")),
                                                ephemeral=True)


    @appcommand(name="tail",
                description="[MOD] Muestra las últimas líneas del archivo de log.")
    @describe(n="La cantidad de líneas del archivo que imprimir.")
    @permisos_de_al_menos_nivel(NivelPermisos.MODERADOR)
    async def log_tail(self, interaccion: "Interaction", n: int=15) -> None:
        "Muestra las últimas N líneas del archivo de log."

        lineas = tail(LOG_PATH, n)
        mensaje = ''.join(lineas)

        if self._menos_de_n_caracteres(mensaje, DISCORD_MAX_CHARS - 10):
            await interaccion.response.send_message(f"```\n{mensaje}```",
                                                    ephemeral=True)
            return

        archivo_log = StringIO(mensaje)
        await interaccion.response.send_message(file=File(archivo_log,
                                                          filename=f"log_{n}_ultimas_lineas.txt"),
                                                ephemeral=True)


    @appcommand(name="flush",
                description="[OWNER] Limpia los contenidos del archivo de log.")
    @es_owner()
    async def log_flush(self, interaccion: "Interaction") -> None:
        "Limpia el archivo de log."

        lineas = 0

        with open(LOG_PATH, mode="rb") as arch:
            lineas += sum(1 for linea in arch if linea.strip())

        with open(LOG_PATH, mode="w") as _:
            ... # Sólo lo abrimos para vaciarlo

        await interaccion.response.send_message(f"Vaciado el archivo de log `{LOG_PATH}`.\n"
                                                f"Se borraron `{lineas}` líneas.",
                                                ephemeral=True)


class CogMisc(CogGeneral):
    "Cog para comandos misceláneos."

    @classmethod
    def grupos(cls) -> "GroupsList":
        "Devuelve la lista de grupos asociados a este Cog."

        return [GrupoLog]


    @appcommand(name="info",
                description="Muestra información sobre el asistente.")
    async def about(self, interaccion: "Interaction") -> None:
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
