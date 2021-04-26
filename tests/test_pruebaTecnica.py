import pruebaTecnica as pt
import unittest
import requests
import json
import sys


class TestPruebaTecnica(unittest.TestCase):
    def setUp(self):
        self.app = pt.app.test_client()


    def testBuscarPatente(self):
        response = self.app.get('http://127.0.0.1:5000/buscar_patente/ACDV999')
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())), 
            {"patente": "ACDV999",
            "id":158179}
        )

    def testBuscarPatenteError(self):
        response = self.app.get('http://127.0.0.1:5000/buscar_patente/a_')
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())), 
            {"error": "La patente debe ser alfanumerica"}
        )



    def testBuscarId(self):
        response = self.app.get('http://127.0.0.1:5000/buscar_id/1545')
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())), 
             {"id": 1545,
            "patente":"AAAH005"}
        )

    def testBuscarIdError(self):
        response = self.app.get('http://127.0.0.1:5000/buscar_id/a')
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())), 
             {"error": "El id debe ser un numero entero"}
        )

    def testBuscarIdErrorExceed(self):
    	response = self.app.get('http://127.0.0.1:5000/buscar_id/9999999999')
    	self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())), 
             {"error": "El id excede el total de patentes"}
        )  


    def testSumarMatriz(self):
        response = self.app.get('http://127.0.0.1:5000/sumar_matriz?r=4&c=3&x=1&y=2&z=2')
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())), 
            {"Suma de la submatriz x, y:": 18}
        )

    def testSumarMatrizError(self):
        response = self.app.get('http://127.0.0.1:5000/sumar_matriz?r=a&c=3&x=1&y=2&z=2')
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())), 
            {"error": "Uno de los parametros ingresado no es numerico"}
        )

    def testSumarMatrizErrorRestriccion(self):
        response = self.app.get('http://127.0.0.1:5000/sumar_matriz?r=0&c=3&x=1&y=2&z=2')
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())), 
            {"error": "Alguno de los parametros ingresados no cumple las restricciones"}
        )



if __name__ == "__main__":
    unittest.main()