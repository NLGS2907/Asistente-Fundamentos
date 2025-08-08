"Interfaz para guías."

from typing import Optional

from discord import Interaction, SelectOption
from discord.ui import Select, select

from ...archivos import GUIA_PATH, lista_carpetas
from ...db.atajos import actualizar_version_guia
from ..ui_general import VistaGeneral


class SelectorGuia(VistaGeneral):
    "Clase de una UI personalizada para cambiar de guías."

    def __init__(self, version_actual: Optional[str]=None) -> None:
        "Inicializa una instancia de 'SelectorGuia'."

        super().__init__(agregar_btn_cerrar=False)

        self.version_actual = version_actual


    @select(placeholder="Seleccione una versión de la guía",
            custom_id="selector_de_guia",
            options=[SelectOption(label=ver) for ver in lista_carpetas(GUIA_PATH)],
            max_values=1)
    async def seleccionar_guia(self, interaccion: Interaction, seleccion: Select) -> None:
        "Muestra y selecciona una versión específica de la guía."

        version_vieja = self.version_actual
        nueva_version = seleccion.values[0] # Debería tener sólo un elemento
        self.version_actual = nueva_version

        actualizar_version_guia(nueva_version, interaccion.message.guild.id)

        formato_log = {"guild": interaccion.guild.name,
                       "old_ver": version_vieja,
                       "new_ver": nueva_version}

        self.log.info("En '%(guild)s', la versión de la guía fue cambiada " % formato_log +
                      "de %(old_ver)s a %(new_ver)s exitosamente" % formato_log)
        await interaccion.response.edit_message(content="**[AVISO]** La versión de la guía " +
                            f"fue cambiada{f' de `{version_vieja}`' if version_vieja else ''} a " +
                            f"`{nueva_version}` exitosamente.",
                                                view=None)
