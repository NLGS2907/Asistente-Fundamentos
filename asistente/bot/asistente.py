"""
Módulo dedicado a contener la clase personalizada 'CustomBot'.
"""

from logging import DEBUG, INFO
from platform import system
from typing import TYPE_CHECKING, Optional, TypeAlias

from discord import Intents, Message, Permissions
from discord.ext.commands import Bot
from discord.utils import utcnow

from ..ahorcado import Ahorcado
from ..archivos import buscar_archivos
from ..db.atajos import actualizar_guild, op_usuario
from ..db.enums import NivelPermisos
from ..logger import AssistLogger

if TYPE_CHECKING:
    from datetime import datetime, timedelta
    from os import PathLike

# Para que no tire error en Windows al cerrar el Bot.
try:
    from asyncio import WindowsSelectorEventLoopPolicy, set_event_loop_policy
    if system() == "Windows":
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())
except ImportError:
    AssistLogger().warning("No se pudo importar 'WindowsSelectorEventLoopPolicy', "
                           "probablemente porque esto no es Windows.")

ASISTENTE_ID: int = 889312376036425810
"El ID del usuario bot que es el Asistente."

COGS_PATH: "PathLike" = "./asistente/cogs"
"La ruta donde viven todos los cogs de comandos."

DiccionarioPartidas: TypeAlias = dict[str, Ahorcado]


# pylint: disable=abstract-method
class Asistente(Bot):
    """
    Clase pasa sobrecargar y agregar cosas a la clase 'Bot'.
    """

    @staticmethod
    def version() -> tuple[int, int, int]:
        """
        Devuelve la versión del asistente como una tupla de 3 numeros del tipo (X, Y, Z),
        indicando una revisión importante, un parche mayor, o un parche menor respectivamente.
        """

        return (2, 0, 0)


    @staticmethod
    def intents_asistente() -> Intents:
        """
        Crea un objeto `Intents` personalizado para este asistente.
        """

        intents = Intents.all()
        return intents


    @staticmethod
    def permisos_preferidos() -> Permissions:
        """
        Devuelve los permisos preferidos por el asistente.
        """

        perms = Permissions.none()

        perms.update(
            send_messages=True,
            manage_messages=True,
            read_message_history=True,
            send_messages_in_threads=True,
            manage_threads=True,
            mention_everyone=True,
            read_messages=True, # También conocido bajo el alias 'View Channels'
            add_reactions=True,
            use_application_commands=True # Discord lo llama 'Use Slash Commands'
        )

        return perms


    def __init__(self,
                 verbose: bool=False,
                 **opciones) -> None:
        """
        Inicializa una instancia de tipo 'Asistente'.

        verbose: Indica si incluir todos los mensajes de logging en la consola, además del archivo.
        opciones: Argumentos extra que elevar al constructor padre del bot.
        """

        super().__init__("!", # Por legacy se eligió esto, pero no se va a usar nunca
                         intents=Asistente.intents_asistente(),
                         application_id=ASISTENTE_ID,
                         options=opciones)

        self.inicializado_en: "datetime" = utcnow()
        "El momento exacto en que el bot fue inicializado."

        self.log: AssistLogger = AssistLogger(nivel_cons=(DEBUG if verbose else INFO))
        "Devuelve el logger del bot."

        self.partidas: DiccionarioPartidas = {}
        "Diccionario donde almacenar las partidas de ahorcado."


    async def setup_hook(self) -> None:
        """
        Reliza acciones iniciales que el bot necesita.
        """

        await self.cargar_cogs()


    async def cargar_cogs(self) -> None:
        """
        Busca y carga recursivamente todos los cogs del bot.
        """

        self.log.info("Cargando cogs:")

        ext = "py"

        for ruta_cog in buscar_archivos(patron=f"*.{ext}",
                                        nombre_ruta=COGS_PATH,
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
