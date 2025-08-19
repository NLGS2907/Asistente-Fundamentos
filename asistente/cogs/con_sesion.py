"Cog general para los casos en los que se tiene una sesión HTTP."

from typing import TYPE_CHECKING

from ..excepciones import SessionNotSetUp
from .general import CogGeneral

if TYPE_CHECKING:
    from discord import Interaction
    from discord.app_commands import AppCommandError

    from ..bot import Asistente


class CogHTTP(CogGeneral):
    """
    Clase de conveniencia para comandos con sesión HTTP.

    Sólo los cogs que incluyan algún comando que depende de _requests_ HTTP deberían
    heredar de esta clase.
    """

    async def interaction_check(self, _interaction) -> bool:
        "Checks especiales a correr antes de cada comando, aparte de los decoradores."

        # Todos los comandos en este Cog van a necesitar, en cierta medida,
        # interactuar con el Backend
        self.bot.sesion_bien_iniciada()

        return True


    def mensaje_error(self, interaccion: "Interaction", error: "AppCommandError") -> str:
        "Muestra el mensaje a mostrar por el chat de Discord en caso de error en este Cog."

        # no se inicio la sesión correctamente
        if self.bot.sesion is None and isinstance(error, SessionNotSetUp):
            return ("La sesión con el backend no parece estar correctamente configurada.\n"
                    "Este comando no estará disponible en este conexto.")

        # se inició la sesión en algún momento, pero ahora mismo está cerrada
        if self.bot.sesion.closed and isinstance(error, SessionNotSetUp):
            return ("La sesión con el backend parece haber sido cerrada prematuramente, por lo "
                    "que no puedo procesar este comando.")

        # si todo falla, le delegamos la lógica al Cog padre
        return super().mensaje_error(interaccion, error)


async def setup(_bot: "Asistente"):
    "Agrega el cog de este módulo al Asistente."

    # Este Cog no está pensado para agregarse.
