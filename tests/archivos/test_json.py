"Módulo para tests de archivos de formato JSON."

from io import StringIO
from unittest import TestCase

from asistente.archivos.json import cargar_json, guardar_json


class TestArchivosJSON(TestCase):
    "Tests de archivos JSON."

    def test_1_caarga_un_json_simple(self) -> None:
        "Carga desde un archivo en memoria un diccionario simple."

        dic_simple = {"a": 1, "b": 2, "c": 3, "d": [4, 5]}
        # NO es lo mismo que `str(dic_simple)`.
        # La sintaxis de JSON requiere que los strings sean de comillas dobles
        dic_str = '{"a": 1, "b": 2, "c": 3, "d": [4, 5]}'
        archivo = StringIO(dic_str)

        dic_final = cargar_json(archivo)

        self.assertEqual(str(dic_final), dic_str.replace("\"", "'"))
        self.assertEqual(str(dic_final), str(dic_simple))
        self.assertEqual(dic_final, dic_simple)


    def test_2_guarda_un_json_simple(self) -> None:
        "Guarda en memoria un archivo JSON simple."

        dic_guardable = {"a": 1, "b": "bb", "c": [1, 2], "d": ["dd", "de"], "e": {"ee": 55}}
        dic_str = r'{"a": 1, "b": "bb", "c": [1, 2], "d": ["dd", "de"], "e": {"ee": 55}}'
        archivo = StringIO() # por ahora vacío

        guardar_json(dic_guardable, archivo, sangria=0)
        archivo.seek(0) # para devolver el cursor del buffer al inicio
        dic_leido = archivo.read().replace("\n", "").replace(",", ", ")

        self.assertEqual(dic_str, dic_leido)
        self.assertEqual(str(dic_guardable), dic_leido.replace("\"", "'"))


    def test_3_no_carga_rutas_incorrectas(self) -> None:
        "Debería fallar si no existe el archivo."

        with self.assertRaises(FileNotFoundError):
            cargar_json("__path_basura__")
