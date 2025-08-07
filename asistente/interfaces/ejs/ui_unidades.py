"""
Interfaz para las Unidades.
"""

from typing import Optional

from discord import Interaction, SelectOption
from discord.ui import Select

from ...archivos import (
    GUIA_DEFAULT,
    DiccionarioGuia,
    cargar_guia,
    lista_unidades,
)
from ..ui_general import VistaGeneral
from .ui_ejercicios import SelectorEjercicios


class MenuSelectorUnidad(Select):
    """
    Clase que representa un menú selector de Unidades, no la interfaz en sí.
    """

    def __init__(
        self,
        *,
        custom_id: str="menu_selector_unidad",
        placeholder: Optional[str]="Seleccione una Unidad",
        min_values: int=1,
        max_values: int=1,
        disabled: bool=False,
        row: Optional[int]=None,
        guia: DiccionarioGuia=cargar_guia(GUIA_DEFAULT)
    ) -> None:
        """
        Inicializa una instacia de 'MenuSelectorUnidad'.
        """

        self.guia = guia

        opciones = [SelectOption(label=f"Unidad {unidad}",
                                 description=self.guia[unidad]["titulo"],
                                 value=unidad)

                                 for unidad in lista_unidades(self.guia)]

        super().__init__(custom_id=custom_id,
                         placeholder=placeholder,
                         min_values=min_values,
                         max_values=max_values,
                         options=opciones,
                         disabled=disabled,
                         row=row)


    async def callback(self, interaccion: Interaction) -> None:
        """
        Procesa la unidad elegida por el usuario del menú selector.
        """

        unidad_elegida = self.values[0]

        vista = SelectorEjercicios(guia=self.guia, unidad=unidad_elegida)
        await interaccion.response.edit_message(content="Elija el ejercicio",
                                                view=vista)


class SelectorUnidad(VistaGeneral):
    """
    Clase de una UI personalizada para seleccionar unidades
    de ejercicios.
    """

    def __init__(self, guia: DiccionarioGuia) -> None:
        """
        Inicializa una instancia de 'SelectorUnidad'.
        """

        super().__init__(agregar_btn_cerrar=False)

        self.add_item(MenuSelectorUnidad(guia=guia))
