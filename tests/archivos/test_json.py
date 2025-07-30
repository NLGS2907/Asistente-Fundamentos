"""
Módulo para tests de archivos de formato JSON.
"""

from os import remove as arch_remove
from unittest import TestCase

from asistente.archivos.json import cargar_json, guardar_json


class TestArchivosJSON(TestCase):
    """
    Tests de archivos JSON.
    """

    def test_1_guarda_y_carga_json_simple(self) -> None:
        """
        Guarda y carga un archivo JSON simple
        """

        arch_temp = "tests/archivos/json_simple.json"
        dic_simple = {'a': 1, 'b': 2, 'c': 3, 'd': [4, 5]}

        guardar_json(dic_simple, arch_temp, sangria=None)

        try:

            with open(arch_temp) as arch:
                dic_simple_str = arch.read()

            dic_cargado = cargar_json(arch_temp)

            self.assertEqual(dic_simple_str, '{"a": 1, "b": 2, "c": 3, "d": [4, 5]}') # Si se guardó bien
            self.assertEqual(dic_cargado, dic_simple) # Si se cargó bien
            with self.assertRaises(FileNotFoundError):
                cargar_json("__path_basura__")

        finally:
            arch_remove(arch_temp)
