"""
Módulo dedicado a contener la clase personalizada 'CustomBot'.
"""

from platform import system
from typing import TYPE_CHECKING, Optional, TypeAlias

from discord import Intents, Message
from discord.ext.commands import Bot
from discord.utils import utcnow

from ..ahorcado import Ahorcado
from ..archivos import buscar_archivos
from ..db.atajos import actualizar_guild, get_asist_id, get_ruta_cogs, op_usuario
from ..db.enums import NivelPermisos
from ..logger import AsistLogger

if TYPE_CHECKING:
    from datetime import datetime, timedelta

# Para que no tire error en Windows al cerrar el Bot.
try:
    from asyncio import WindowsSelectorEventLoopPolicy, set_event_loop_policy
    if system() == "Windows":
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())
except ImportError:
    AsistLogger().warning("No se pudo importar 'WindowsSelectorEventLoopPolicy', "
                           "probablemente porque esto no es Windows.")

DiccionarioPartidas: TypeAlias = dict[str, Ahorcado]


# pylint: disable=abstract-method
class Asistente(Bot):
    """
    Clase pasa sobrecargar y agregar cosas a la clase 'Bot'.
    """


    @staticmethod
    def intents_asistente() -> Intents:
        """
        Crea un objeto `Intents` personalizado para este asistente.
        """

        intents = Intents.all()
        return intents


    def __init__(self,
                 **opciones) -> None:
        """
        Inicializa una instancia de tipo 'Asistente'.
        """

        super().__init__("!", # Por legacy se eligió esto, pero n ose va a usar nunca
                         intents=Asistente.intents_asistente(),
                         application_id=get_asist_id(),
                         options=opciones)

        self.inicializado_en: "datetime" = utcnow()
        "El momento exacto en que el bot fue inicializado."

        self.log: AsistLogger = AsistLogger()
        "Devuelve el logger del bot."

        self.partidas: DiccionarioPartidas = {}
        "Diccionario donde almacenar las partidas de ahorcado."


    async def setup_hook(self) -> None:
        """
        Reliza acciones iniciales que el bot necesita.
        """

        sep = "=" * 25
        self.log.info(f"{sep} Iniciando Asistente {sep}")

        await self.cargar_cogs()


    async def cargar_cogs(self) -> None:
        """
        Busca y carga recursivamente todos los cogs del bot.
        """

        self.log.info("Cargando cogs:")

        ext = "py"

        for ruta_cog in buscar_archivos(patron=f"*.{ext}",
                                        nombre_ruta=get_ruta_cogs(),
                                        ignorar_patrones=("__init__.*", "*_abc.*", "general.")):

            self.log.debug(f"[COG] Cargando cog {ruta_cog!r}")
            await self.load_extension(ruta_cog.removesuffix(f".{ext}").replace("/", "."))

        self.log.info("Sincronizando arbol de comandos...")
        await self.tree.sync()


    def actualizar_db(self) -> None:
        """
        Hace todos los procedimientos necesarios para actualizar
        la base de datos de ser necesario.
        """

        self.log.info("[DB] Actualizando guilds...")
        for guild in self.guilds:
            if not actualizar_guild(guild.id, guild.name):
                self.log.info(f"[DB] Nuevo Guild '{guild.name}' detectado y registrado en DB")

            # Por definición, el dueño del servidor siempre tiene permisos
            owner_perms: Optional[NivelPermisos] = op_usuario(guild.owner_id,
                                                              NivelPermisos.ADMINISTRADOR,
                                                              guild.id)

            if owner_perms is None:
                self.log.info(f"[DB] Guild '{guild.name}' no tiene al dueño actual registrado"
                              " en la lista de permisos."
                              f" Registrado el usuario '{guild.owner.global_name}'")

            # El dueño no tenía el nivel más alto de permisos por algún motivo
            elif owner_perms.inferior_a(NivelPermisos.ADMINISTRADOR):
                self.log.warning(f"[DB] El usuario dueño '{guild.owner.global_name}' del"
                                 f" guild '{guild.name}' no tenía el nivel más alto de permisos."
                                 " Se cambió el permiso a administrador.")

    @property
    def uptime(self) -> "timedelta":
        """
        Muestra cuánto tiempo el bot lleva activo.
        """

        return utcnow() - self.inicializado_en


    @staticmethod
    def es_ultimo_mensaje(msg: Message) -> bool:
        """
        Verifica que el mensaje a procesar no sea el
        ultimo del canal.
        """

        return msg == msg.channel.last_message


    def es_mensaje_de_bot(self, msg: Message) -> bool:
        """
        Verifica si un mensaje pasado es un mensaje escrito
        por el bot.
        """

        return not self.es_ultimo_mensaje(msg) and msg.author == self.user


    def encontrar_partida(self, id_a_encontrar: str) -> Optional[Ahorcado]:
        """
        Si la encuentra dentro del diccionario de partidas, devuelve la partida
        que corresponde al ID pasado.
        """

        partida_a_devolver = None

        for id_partida, partida in self.partidas.items():

            if str(id_a_encontrar) == id_partida:

                partida_a_devolver = partida
                break

        return partida_a_devolver
