"Modal para ingresar un alumno en el sistema."

from typing import TYPE_CHECKING

from discord import Interaction
from discord.enums import TextStyle
from discord.ui import Modal, TextInput

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

        await interaccion.response.send_message(f"_Procesando padrón `{self.padron.value}`..._",
                                                ephemeral=True)
