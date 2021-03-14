import copy
from itertools import permutations, takewhile, chain
class Atomico:
    def __init__(self,nombre, representacion, alineacion):
        self.nombre = nombre
        self.representacion = representacion
        self.alineacion = alineacion

    def __str__(self):
        return "Tipo: {}, Rep: {}, Ali: {}".format(self.nombre,self.representacion, self.alineacion)

class Structs:
    def __init__(self, nombre, elementos, representacion= None, alineacion = None, elementos_optimo = None, desperdicio = None):
        self.nombre = nombre
        self.elementos = elementos
        self.representacion = representacion
        self.alineacion = alineacion
        self.desperdicio = desperdicio
        self.elementos_optimo = elementos_optimo


atomicos = dict()
registros = dict()




def es_valida(opcion):
    opcion = opcion.split(" ")
    if len(opcion) < 2:
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
            if elem not in atomicos.keys() and elem not in registros.keys():
                print("Ha introducido un tipo no existente")
                return
        nuevos_elementos = []

        for elem in opcion[2:]:
            try:
                nuevos_elementos.append(atomicos[elem])
            except:
                nuevos_elementos.append(registros[elem])       
        nuevo_registro = Structs(opcion[1], nuevos_elementos)
        registros[opcion[1]] = nuevo_registro

def split_array(arreglo):
    matriz = []
    numerito = 0
    while numerito != len(arreglo):
        to_append = arreglo[numerito:numerito+4]
        matriz.append(to_append)
        numerito = numerito + 4
    print(matriz)

def calcular_tamano_y_perdida(array):
    return len(array), array.count(0)


def crear_espacio_sin_reglas(array,resultado ):
    array = array[::-1]

    while array:
        elemento = array.pop()
        counter = int(elemento.representacion)
        nombre = elemento.nombre
        while counter:
            resultado.append(nombre)
            counter -= 1
    return resultado
  #  while len(resultado) % 4 != 0:
  #      resultado.append(0)

def crear_espacio_con_reglas(array, resultado):
    
    array = array[::-1]
    
    while array:
        elemento = array.pop()
        counter = int(elemento.representacion)
        alineacion = int(elemento.alineacion)
        nombre = elemento.nombre 
             
       # if not(resultado):
       #     while counter:
       #         resultado.append(nombre)
       #         counter -= 1
       # else:
        if len(resultado) % alineacion == 0:
            if nombre in atomicos.keys():
                while counter:
                    resultado.append(elemento)
                    counter -= 1
            else:
                for elem in elemento.elementos_optimo:
                    if elem != 0:
                        resultado.append(elemento)
                    else:
                        resultado.append(elem)
                
        else:
            while len(resultado) % alineacion != 0 :
                resultado.append(0)
            if nombre in atomicos.keys():
                while counter:
                    resultado.append(elemento)
                    counter -= 1
            else:
                for elem in elemento.elementos_optimo:
                    if elem != 0:
                        resultado.append(elemento)
                    else:
                        resultado.append(elem)
             
                   
          
                
    #while len(resultado) % 4 != 0:
    #    resultado.append(0)
   # print(resultado)
   # split_array(resultado)
    return resultado



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
def verificar_hay_struct(array):
    resultado = []
    for elem in array:
        if elem.nombre in registros.keys():
            resultado.append(elem)
    return resultado
#def multiples_opciones(elemento, resultado, arreglo, ya_evaluados, recursion_level):
       
#        counter = int(elemento.representacion)
#        alineacion = int(elemento.alineacion)
#        nombre = elemento.nombre        
#        if not(resultado):
#            while counter:
#                resultado.append(nombre)
#                counter -= 1
#        else:
#            if len(resultado) % alineacion == 0:
#                print(elemento)
#                while counter:
#                    resultado.append(nombre)
#                    counter -= 1
#            else:
#                print("extendiendo con 0s", elemento)
#                while len(resultado) % alineacion != 0 :
#                    resultado.append(0)
#                while counter:
                    
 #                   resultado.append(nombre)
 #                   counter -= 1
                    
#        ya_evaluados.append(elemento)
        
#        for elem in arreglo:           
#            if not(verificar_nombres(elem, ya_evaluados)):                
#                print("holi soy un elem", elem,"mi padre es:", elemento, "recursion level:", recursion_level)
#                multiples_opciones(elem, resultado, arreglo, ya_evaluados, recursion_level+1)
#        print(resultado)
#        return resultado
                
                
   # while len(resultado) % 4 != 0:
   #     resultado.append(0)
   # print(resultado)
   # split_array(resultado)

def determina_optimo(array):
    
    resultado = array[0]
    for elem in array:
        numero = elem.count(0)
        if(numero < resultado.count(0)):
            resultado = elem      
    return resultado, len(resultado), resultado.count(0), resultado[0].alineacion


def backtracking(nombre):
    resultado = []
    if nombre in registros.keys():
        arreglo = copy.deepcopy(registros[nombre].elementos)
        for lista in list(permutations(arreglo)):               
            webito = crear_espacio_con_reglas(list(lista), [])
            resultado.append(webito)
    return determina_optimo(resultado)

def equals_cero(x):
    return x == 0

def revisar_ceros(array, elem):
   # array = array[::-1]
    resultado = dict()
    i = 0
    while i< len(array):
        x = array[i-1]
        if(array[i] == 0):
            contador = 0
            while array[i] == 0:
                contador += 1
                i += 1
            resultado[x] = contador
        else:
            i += 1
    return resultado
    
  #  i = 0
  #  while i < len(array):
  #      if array[i] != 0:
  #          i = i+1
  #          continue
  #      nuevo_array = list(takewhile(equals_cero, array[i:]))
        
  #      i = len(nuevo_array) + i

  #      resultado[array[len(nuevo_array)-i-1]] = len(nuevo_array)
  #  print(resultado)
   
def describir(nombre):
    
    if nombre in registros.keys():
        a_evaluar = registros[nombre].elementos
        #Espacio sin reglas:
        structs = verificar_hay_struct(a_evaluar)


      #  if(structs):
      #      for elem in structs:
                #elem.representacion = len(crear_espacio_sin_reglas(elem.elementos, []))
      #          elem.elementos_optimo = crear_espacio_con_reglas(elem.elementos,[])
      #          elem.representacion = len(elem.elementos_optimo)
      #          elem.alineacion = elem.elementos[0].alineacion
            
      #  print(crear_espacio_con_reglas(a_evaluar, []))
        if(structs):
            for elem in structs:
                elem.elementos_optimo, elem.representacion, elem.desperdicio, elem.alineacion = backtracking(elem.nombre)

                for webo in elem.elementos_optimo:
                    try:
                        print(webo.nombre)
                    except:
                        print(webo)


            registros[nombre].elementos_optimo,registros[nombre].representacion,registros[nombre].desperdicio,registros[nombre].alineacion = backtracking(nombre)
            print(registros[nombre].elementos_optimo)
            for elem in registros[nombre].elementos_optimo:                
                try:
                    print(elem.nombre)
                except:
                    print(elem)
                #
                #
                
                #elem.saltos = revisar_ceros(elem.elementos_optimo, elem)
      #  else:
      #      print(crear_espacio_sin_reglas(a_evaluar, []))

      #      print(crear_espacio_con_reglas(a_evaluar, []))
      #      backtracking(nombre)
        
        
        #crear_espacio_con_reglas(registros[nombre[1]], [])
       # backtracking(nombre)



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
               # print_structs()
            elif(opcion[0].lower() == "describir"):
                describir(opcion[1])
              
            elif(opcion[0].lower() == "salir"):
                break
        else:
            print("Por favor introduzca una opcion valida")

   



if __name__ == '__main__':
    main()