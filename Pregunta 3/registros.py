import copy
from itertools import permutations
class Atomico:
    def __init__(self,nombre, representacion, alineacion):
        self.nombre = nombre
        self.representacion = representacion
        self.alineacion = alineacion

    def __str__(self):
        return "Tipo: {}, Rep: {}, Ali: {}".format(self.nombre,self.representacion, self.alineacion)

atomicos = dict()
registros = dict()


def es_valida(opcion):
    opcion = opcion.split(" ")
    if len(opcion)< 2:
        return False
    
    if opcion[0].lower() != "atomico" and opcion[0].lower() != "struct" and opcion[0].lower() != "describir": 
        return False
    if opcion[0].lower() == "atomico":
        if(len(opcion) > 4):            
            return False
        if opcion[2].isdigit() and opcion[3].isdigit():
            return True
    if opcion[0].lower() == "struct":
        if len(opcion) < 3:
            return False
        return True
    if opcion[0].lower() == "describir":
        return True

def print_atomicos():
    for key, value in atomicos.items():
        print( key,value)

def print_structs():
    for key, values in registros.items():
        print("Struct:", key)
        for value in values:
            print(value)

def ya_existente(opcion):
    if (opcion[1] in atomicos.keys() or opcion[1] in registros.keys()):
        print("Nombre ya existente") 
        return True 

def crear_atomico(opcion):
    if(not(ya_existente(opcion))):          
        atomicos[opcion[1]] = Atomico(opcion[1],opcion[2], opcion[3])
    
def crear_registro(opcion):
    if(not(ya_existente(opcion))): 
        for elem in opcion[2:]: 
            if elem not in atomicos.keys():
                print("Ha introducido un tipo no existente")
                return
        nuevos_atomicos = []

        for elem in opcion[2:]:
            nuevos_atomicos.append(atomicos[elem])

        registros[opcion[1]] = copy.deepcopy(nuevos_atomicos)

def split_array(arreglo):
    matriz = []
    numerito = 0
    while numerito != len(arreglo):
        to_append = arreglo[numerito:numerito+4]
        matriz.append(to_append)
        numerito = numerito + 4
    print(matriz)

def crear_espacio_sin_reglas(nombre,resultado = []):
    array = registros[nombre]
    array = array[::-1]

    while array:
        print(array)
        elemento = array.pop()
        counter = int(elemento.representacion)
        nombre = elemento.nombre
        while counter:
            resultado.append(nombre)
            counter -= 1
    while len(resultado) % 4 != 0:
        resultado.append(0)

def crear_espacio_con_reglas(array, resultado):
    
    array = array[::-1]

    while array:
        elemento = array.pop()
        counter = int(elemento.representacion)
        alineacion = int(elemento.alineacion)
        nombre = elemento.nombre        
        if not(resultado):
            while counter:
                resultado.append(nombre)
                counter -= 1
        else:
            if len(resultado) % alineacion == 0:
                while counter:
                    resultado.append(nombre)
                    counter -= 1
            else:
                while len(resultado) % alineacion != 0 :
                    resultado.append(0)
                while counter:
                    resultado.append(nombre)
                    counter -= 1
                
    while len(resultado) % 4 != 0:
        resultado.append(0)
    print(resultado)
    split_array(resultado)
    



   # while array:
   #     elemento = array.pop()
   ##     counter = int(elemento.representacion)
    #    tamano = 0
        
    #    nombre = elemento.nombre
      #  while counter != 0:
       #     if counter % 4 == 0:
       #         resultado.append([0,0,0,0])
       #         for j in range(counter):
       #             resultado[len(resultado)-1][j] = nombre
         


      #  if i % 4 == 0:
      #      resultado.append([0,0,0,0])
      #      for j in range(3):
      #      resultado[len(resultado)-1][j] = nombre

def verificar_nombres(elem, array):
    for elemento in array:
        if elem.nombre == elemento.nombre:
            return True
    return False



def multiples_opciones(elemento, resultado, arreglo, ya_evaluados, recursion_level):
       
        counter = int(elemento.representacion)
        alineacion = int(elemento.alineacion)
        nombre = elemento.nombre        
        if not(resultado):
            while counter:
                resultado.append(nombre)
                counter -= 1
        else:
            if len(resultado) % alineacion == 0:
                print(elemento)
                while counter:
                    resultado.append(nombre)
                    counter -= 1
            else:
                print("extendiendo con 0s", elemento)
                while len(resultado) % alineacion != 0 :
                    resultado.append(0)
                while counter:
                    
                    resultado.append(nombre)
                    counter -= 1
                    
        ya_evaluados.append(elemento)
        
        for elem in arreglo:           
            if not(verificar_nombres(elem, ya_evaluados)):                
                print("holi soy un elem", elem,"mi padre es:", elemento, "recursion level:", recursion_level)
                multiples_opciones(elem, resultado, arreglo, ya_evaluados, recursion_level+1)
        print(resultado)
        return resultado
                
                
   # while len(resultado) % 4 != 0:
   #     resultado.append(0)
   # print(resultado)
   # split_array(resultado)

def backtracking(nombre):
    resultado2 = []
    if nombre[1] in registros.keys():
        arreglo = copy.deepcopy(registros[nombre[1]])
        print("holis",arreglo)
        print(list(permutations(arreglo)))
        
        for lista in list(permutations(arreglo)):            
            for elem in lista:
                y = []
                x = []
                
                webito = multiples_opciones(elem, x, lista, y,0)
                if webito not in resultado2:
                    resultado2.append(webito)
    print("resultadito: ",resultado2)

    
    
    
def describir(nombre):
   
    if nombre[1] in registros.keys():
       # crear_espacio_sin_reglas(nombre[1], [])
        crear_espacio_con_reglas(registros[nombre[1]], [])
        backtracking(nombre)



def main():
    print("Bienvenido, por favor introduzca una de las opciones")
    opcion = ""
    while True:
        print("Introduzca ATOMICO <nombre> <representacion> <alineacion> para crear un nuevo tipo atomico")
        print("Introduzca STRUCT <nombre> [<tipo>] para crear un nuevo struct")
        print("Introduzca DESCRIBIR <nombre> para describir un registro ya existente")
        opcion = input()
        if(es_valida(opcion)):
            opcion = opcion.split(" ")

            if(opcion[0].lower() == "atomico"):                
                crear_atomico(opcion)
                print_atomicos()
            elif(opcion[0].lower() == "struct"):
                crear_registro(opcion)
                print_structs()
            elif(opcion[0].lower() == "describir"):
                describir(opcion)
              
            elif(opcion[0].lower() == "salir"):
                break
        else:
            print("Por favor introduzca una opcion valida")

   



if __name__ == '__main__':
    main()