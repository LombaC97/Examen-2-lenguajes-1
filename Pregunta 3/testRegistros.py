from registros import *
import unittest
from collections import Counter
from io import StringIO
from unittest.mock import patch

class TestRegistrosMethods(unittest.TestCase):
    #Verificamos instancia de atomico
    def test_1(self):
        entrada = "ATOMICO int 4 4"
        entrada = entrada.split(" ")
        crear_atomico(entrada)
        self.assertIsInstance(atomicos["int"], Atomico)

    #Verificamos instancia de struct
    def test_2(self):
        entrada = "STRUCT prueba int"
        entrada = entrada.split(" ")
        crear_registro(entrada, "struct")
        self.assertIsInstance(registros["prueba"], Struct)

    #Verificamos instancia de union
    def test_3(self):
        entrada = "UNION prueba2 int"
        entrada = entrada.split(" ")
        crear_registro(entrada, "union")
        self.assertIsInstance(variantes["prueba2"], Union)
    #Usamos un elemento atomico ya craedo (el int) y verificamos que sea correcto su tamano y alineacion
    def test_4(self):
        resultado =  describir("int")
        self.assertEqual(resultado, "Soy un registro atomico de nombre: int, mi representacion es de 4 bytes y mi alineacion es de 4 bytes")

    # Test struct sencillo con solamente un int, debe haber una perdida total de 0 bytes en todos los casos
    def test_5(self):
       
        with patch('sys.stdout', new=StringIO()) as mocked_stdout:
            describir("prueba")
            output = mocked_stdout.getvalue()  
        #Verificamos que el output contenga los strings de los resultados esperados
        empaquetado = "Para el caso empaquetado hubo un total de 4 bytes ocupados, y una perdida de 0 bytes"
        no_empaquetado =  "Para el caso no empaquetado hubo un total de 4 bytes ocupados, y una perdida total de 0 bytes"
        optimizado = "Me encuentro en la posicion 0, Soy un registro atomico de nombre: int, mi representacion es de 4 bytes y mi alineacion es de 4 bytes"

        self.assertTrue(empaquetado in output and no_empaquetado in output and optimizado in output) 

    #Test variante sencillo con solamente un int, su representacion debe ser 4 bytes y su alineacion tambien a 4
    def test_6(self):
        with patch('sys.stdout', new=StringIO()) as mocked_stdout:
            describir("prueba2")
            output = mocked_stdout.getvalue()  
        #Verificamos que el output contenga los strings de los resultados esperados
        expected_output = "Soy un registro variante, mi tamano es de: 4 bytes, y mi alineacion en caso de estar en un struct seria 4"
        self.assertTrue(expected_output in output)

    #Crearemos ahora un struct mas complejo que tenga int 4 4 y char 2 2. Ver output en consola para corroborar
    def test_7(self):
        crear_atomico("ATOMICO char 2 2".split(" "))
        crear_registro("STRUCT prueba3 char int".split(" "), "struct")
        with patch('sys.stdout', new=StringIO()) as mocked_stdout:
            describir("prueba3")
            output = mocked_stdout.getvalue()
         #Resultados esperados
        empaquetado = "Para el caso empaquetado hubo un total de 6 bytes ocupados, y una perdida de 0 bytes"
        no_empaquetado =  "Para el caso no empaquetado hubo un total de 8 bytes ocupados, y una perdida total de 2 bytes"
        optimizado = "Para el caso optimizado hubo un total de 6 bytes ocupados, y una perdida total de 0 bytes"
        print(output)
        #Verificamos que el output contenga los strings de los resultados esperados
        self.assertTrue(empaquetado in output and no_empaquetado in output and optimizado in output)  
    #Crearemos ahora un registro variante mas complejo y verificaremos cual sera su alineacion y representacion
    def test_8(self):
        crear_atomico("ATOMICO float 8 8".split(" "))
        crear_atomico("ATOMICO bool 1 2".split(" "))
        crear_registro("UNION prueba4 float bool".split(" "),"union")
        with patch('sys.stdout', new=StringIO()) as mocked_stdout:
            describir("prueba4")
            output = mocked_stdout.getvalue()
        #Resultados esperados
        expected_output = "Soy un registro variante, mi tamano es de: 8 bytes, y mi alineacion en caso de estar en un struct seria 8"
        self.assertTrue(expected_output in output)

    #Crearemos ahora un struct con otro struct dentro ( el previamente creado )
    def test_9(self):
        crear_registro("STRUCT prueba5 bool prueba3".split(" "),"struct")
        with patch('sys.stdout', new=StringIO()) as mocked_stdout:
            describir("prueba5")
            output = mocked_stdout.getvalue()
        print(output)
        
        #Resultados esperados
        empaquetado = "Para el caso empaquetado hubo un total de 7 bytes ocupados, y una perdida de 0 bytes"
        no_empaquetado =  "Para el caso no empaquetado hubo un total de 10 bytes ocupados, y una perdida total de 3 bytes"
        optimizado = "Para el caso optimizado hubo un total de 8 bytes ocupados, y una perdida total de 1 bytes"
        #Verificamos que el output contenga los strings de los resultados esperados
        self.assertTrue(empaquetado in output and no_empaquetado in output and optimizado in output)

    #Crearemos ahora un union con otro union dentro y otro struct. En este caso veremos que ocurre si el struct esta empaquetado
    #No empaquetado y optimizado
    def test_91(self):
        crear_atomico("ATOMICO nose 2 3".split(" "))
        crear_registro("UNION prueba6 nose prueba4 prueba3".split(" "), "union")
        with patch('sys.stdout', new=StringIO()) as mocked_stdout:
            describir("prueba6")
            output = mocked_stdout.getvalue()
        print(output)
        
        #Resultados esperados
        empaquetado = "Soy un registro variante, mi tamano es de: 8 bytes, y mi alineacion en caso de estar en un struct seria None"
        no_empaquetado =  "Soy un registro variante, mi tamano es de: 8 bytes, y mi alineacion en caso de estar en un struct seria 24"
        optimizado = "Soy un registro variante, mi tamano es de: 8 bytes, y mi alineacion en caso de estar en un struct seria 24"
        #Mas resultados esperados
        struct_empaquetado = "Soy un registro interno, mi tamano es de: 6 bytes, y mi alineacion en caso de estar en un struct seria 4. Bytes desperdiciados en mi: 0"
        struct_no_empaquetado = "Soy un registro interno, mi tamano es de: 8 bytes, y mi alineacion en caso de estar en un struct seria 2. Bytes desperdiciados en mi: 2"
        struct_optimizado = "Soy un registro interno, mi tamano es de: 6 bytes, y mi alineacion en caso de estar en un struct seria 4. Bytes desperdiciados en mi: 0"
        #Verificamos que el output contenga los strings de los resultados esperados
        self.assertTrue(empaquetado in output and no_empaquetado in output and optimizado in output and struct_no_empaquetado in output and struct_empaquetado in output and struct_optimizado in output)
if __name__ == '__main__':
    unittest.main()
