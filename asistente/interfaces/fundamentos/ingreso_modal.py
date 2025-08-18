"Modal para ingresar un alumno en el sistema."

from typing import TYPE_CHECKING

from discord import Interaction
from discord.enums import TextStyle
from discord.ui import Modal, TextInput

from ...auxiliar import (
    INERNAL_SERVER_ERROR,
    INVALID_PADRON,
    MISSING_PADRON,
    NO_CURRENT_CUATRI,
    procesar_padron,
)

if TYPE_CHECKING:
    from ...bot import Asistente


class ModalIngreso(Modal):
    "Modal para ingresar un alumno."

    padron: TextInput = TextInput(
        label="Ingrese su padrón/legajo:",
        style=TextStyle.short,
        custom_id="student_enter_modal_input",
        placeholder="123456",
        min_length=5,
        max_length=6,
        required=True,
        row=0
    )


    def __init__(self, bot: "Asistente") -> None:
        "Inicializa una instancia de este modal."

        super().__init__(timeout=None,
                        title="",
                        custom_id="student_enter_modal")

        self.bot: "Asistente" = bot


    async def on_submit(self, interaccion: "Interaction") -> None:
        "Procesa el padrón ingresado."

        # seguro que la sesión no es `None` a este punto
        async with self.bot.sesion.get("/students/exists",
                                       params=dict(padron=self.padron.value)) as response:
            body: dict = await response.json()
            not_found = f"No se encontró un padrón con el valor `{self.padron.value}`."

            match response.status:
                case 200:
                    if not body.get("exists", False):
                        msg = not_found
                    else:
                        msg = await procesar_padron(self.padron.value,
                                                    body["practica"],
                                                    interaccion)

                case 404:
                    msg = not_found

                case 400:
                    msg = f"**[ERROR]** {self._mensaje_400(body)}"

                case 500:
                    msg = f"**[ERROR]** {self._mensaje_500(body)}"

                case _:
                    msg = (f"El Backend tiró status `{response.status}`, lo cual no es contemplado "
                           "por el asistente. Se ignora.")

            await interaccion.response.send_message(content=msg, ephemeral=True)


    @staticmethod
    def _mensaje_400(response_body: dict) -> str:
        "Devuelve el mensaje en caso de que la respuesta tenga código 400."

        code = response_body.get("code")
        if code == MISSING_PADRON:
            return "No se especificó un padrón."

        if code == INVALID_PADRON:
            return "El padrón no tiene un formato válido."

        return "Ocurrió un error de usuario desconocido."


    @staticmethod
    def _mensaje_500(response_body: dict) -> str:
        "Devuelve el mensaje en caso de que la respuesta tenga código 500."

        code = response_body.get("code")
        if code == NO_CURRENT_CUATRI:
            return ("No hay un cuatrimestre actual configurado en la API, por lo que no "
                    "se encontró nada.")

        if code == INERNAL_SERVER_ERROR:
            return "Ocurrió un error del lado del servidor."

        return "Error de servidor desconocido."
