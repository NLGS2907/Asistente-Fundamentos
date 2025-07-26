"""
Módulo para contener Embeds personalizados.
"""

from typing import Union, TypeAlias

from discord import Colour, Embed

Lineas: TypeAlias = list[str]
"""
Lista de líneas, pensadas para que cada elemento de la lista sea una cadena
separada de las demás por un salto de línea. '`\\n`'.
"""
CamposDict: TypeAlias = dict[str, list[str]]
OpcionesDict: TypeAlias = dict[str, Union[Lineas, CamposDict]]
FormatosDict: TypeAlias = dict[str, str]
"""
Diccionario de la forma "{clave}": "valor", tal que se le pueda aplicar `.format()` después.
"""


class Embebido(Embed):
    """
    Clase de embebido personalizada.
    """

    def __init__(self,
                 *,
                 opciones: OpcionesDict,
                 formatos: FormatosDict=None) -> None:
        """
        Inicializa una instancia de 'Embebido'.
        """

        self.formatos = {} if formatos is None else formatos

        titulo: Lineas = opciones.get("titulo", [])
        descripcion: Lineas = opciones.get("descripcion", [])
        color: int = opciones.get("color", Colour.dark_grey())
        campos: CamposDict = opciones.get("campos", {})
        pie: Lineas = opciones.get("pie", [])

        super().__init__(title=self.custom_format(Embebido.unir(titulo)),
                         description=self.custom_format(Embebido.unir(descripcion)),
                         colour=color)

        for nombre, valores in campos.items():

            self.add_field(name=self.custom_format(nombre),
                           value=self.custom_format(Embebido.unir(valores)),
                           inline=False)

        self.set_footer(text=self.custom_format(Embebido.unir(pie)))


    @staticmethod
    def unir(lista: list[str]) -> str:
        """
        Une los strings de una lista con nuevas líneas.
        """

        return '\n'.join(lista) if lista else ''

    def custom_format(self, cadena: str) -> str:
        """
        Formatea una cadena de manera personalizada.
        """

        for clave, valor in self.formatos.items():

            cadena = cadena.replace('{' + clave + '}', valor)

        return cadena
