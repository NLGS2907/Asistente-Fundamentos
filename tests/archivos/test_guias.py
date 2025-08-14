"Módulo para tests de archivos de guías."

from unittest import TestCase

from asistente.archivos.guias import (
    archivos_guia,
    cargar_guia,
    lista_ejercicios,
    lista_unidades,
    version_es_valida,
)


class TestGuias(TestCase):
    "Tests de archivos de guías de ejercicios."

    def test_1_valida_version(self) -> None:
        "Valida si hay versiones con nombres correctos."

        self.assertTrue(version_es_valida("2019C2"))
        self.assertFalse(version_es_valida("3ex2801"))


    def test_2_valida_estructura_guia(self) -> None:
        "Debería haber exactamente 17 archivos JSON."

        set_archivos = archivos_guia("2019C2", "guia")
        set_esperado = {"guia_1.json",
                        "guia_2.json",
                        "guia_3.json",
                        "guia_4.json",
                        "guia_5.json",
                        "guia_6.json",
                        "guia_7.json",
                        "guia_8.json",
                        "guia_9.json",
                        "guia_10.json",
                        "guia_11.json",
                        "guia_12.json",
                        "guia_13.json",
                        "guia_14.json",
                        "guia_15.json",
                        "guia_16.json",
                        "guia_17.json"}

        self.assertEqual(set_archivos, set_esperado)
        self.assertEqual(archivos_guia("2x2019", "guia"), None)
        with self.assertRaises(FileNotFoundError):
            archivos_guia("2019C2", "guiasa")


    def test_3_carga_una_guia_correctamente(self) -> None:
        "Carga un ejercicio y verifica que esté correcto."

        guia_cargada = cargar_guia("2019C2", "guia")
        enunciado_esperado = {"titulo": [],
                            "descripcion": [
                            "Escribir una función que reciba dos números y devuelva su producto."
                            ],
                            "campos": {},
                            "pie": []}

        with self.assertRaises(FileNotFoundError):
            cargar_guia("2019C2", "guiasa")

        self.assertEqual(cargar_guia("2x2019", "guia"), None)
        self.assertEqual(guia_cargada["1"]["1"], enunciado_esperado)


    def test_4_cuenta_las_unidades_de_una_guia(self) -> None:
        "Deberían ser 17 unidades."

        lista_cargada = lista_unidades(cargar_guia("2019C2", "guia"))
        lista_esperada = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
                          "14", "15", "16", "17"]

        self.assertEqual(lista_cargada, lista_esperada)
        self.assertNotEqual(lista_unidades({"version": "Ninguna, lol",
                                            "10": "judías", "40": 41, "337": "banana"}),
                            lista_esperada)
        with self.assertRaises(KeyError):
            lista_unidades({"10": "judías", "40": 41, "337": "banana"})


    def test_5_cuenta_los_ejercicios_de_una_unidad(self) -> None:
        "Cuenta los ejercicios de la unidad 15. Deberían de ser 13."

        guia_cargada = cargar_guia("2019C2", "guia")
        lista_cargada = lista_ejercicios(guia_cargada, "15")
        lista_esperada = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]

        self.assertEqual(lista_cargada, lista_esperada)
        with self.assertRaises(KeyError):
            lista_ejercicios(guia_cargada, "18")
