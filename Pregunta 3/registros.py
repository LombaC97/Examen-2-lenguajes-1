import copy
import functools
from itertools import permutations, takewhile, chain
class Atomico:
    def __init__(self,nombre, representacion, alineacion):
        self.nombre = nombre
        self.representacion = representacion
        self.alineacion = alineacion

    def __str__(self):
        return "Soy un registro atomico de nombre: {}, mi representacion es de {} bytes y mi alineacion es de {} bytes".format(self.nombre,self.representacion, self.alineacion)

class Struct:
    def __init__(self, nombre, elementos, representacion= None, alineacion = None, elementos_optimo = None, desperdicio = None):
        self.nombre = nombre
        self.elementos = elementos
        self.representacion = representacion
        self.alineacion = alineacion
        self.desperdicio = desperdicio
        self.elementos_optimo = elementos_optimo

class Union:
    def __init__(self, nombre, elementos, representacion = None, alineacion = None):
        self.nombre = nombre
        self.elementos = elementos
        self.representacion = representacion
        self.alineacion = alineacion


atomicos = dict()
registros = dict()
variantes = dict()




def es_valida(opcion):
    opcion = opcion.strip()
    opcion = opcion.split(" ")
    if opcion[0].lower() == "salir":
        return True
    if len(opcion) < 2:
        return False    
    if opcion[0].lower() != "atomico" and opcion[0].lower() != "struct" and opcion[0].lower() != "describir" and opcion[0].lower() != "union": 
        return False
    if opcion[0].lower() == "atomico":
        if(len(opcion) > 4):            
            return False
        if opcion[2].isdigit() and opcion[3].isdigit():
            return True
    if opcion[0].lower() == "struct" or opcion[0].lower() == "union":
        if len(opcion) < 3:
            return False
        return True
    if opcion[0].lower() == "describir":
        return True

def ya_existente(opcion):
    if ( opcion[1] in atomicos.keys() or opcion[1] in registros.keys() or opcion[1] in variantes.keys() ):
        print("Nombre ya existente") 
        return True 

def crear_atomico(opcion):
    if(not(ya_existente(opcion))):          
        atomicos[opcion[1]] = Atomico(opcion[1],opcion[2], opcion[3])
    
def nivel_anidamiento(opcion):
    
    for elem in opcion[2:]:
        try:
                analizar = atomicos[elem]
        except:
                try:
                    analizar = registros[elem]  
                except:
                    analizar = variantes[elem] 
        if type(analizar) is Struct or type(analizar) is Union:
            if(verificar_hay_struct(analizar.elementos) or verificar_hay_union(analizar.elementos)):
                return True
    return False

def crear_registro(opcion, tipo):
    if (nivel_anidamiento(opcion)):
        return print("Excedido el maximo nivel de anidamiento permitido")
    if not(ya_existente(opcion)): 
        for elem in opcion[2:]: 
            if elem not in atomicos.keys() and elem not in registros.keys() and elem not in variantes.keys():
                print("Ha introducido un tipo no existente")
                return
        nuevos_elementos = []

        for elem in opcion[2:]:
            try:
                nuevos_elementos.append(atomicos[elem])
            except:
                try:
                    nuevos_elementos.append(registros[elem])   
                except:
                    nuevos_elementos.append(variantes[elem])    
        if(tipo == "struct"):
            nuevo_registro = Struct(opcion[1], nuevos_elementos)
            registros[opcion[1]] = nuevo_registro
        else:
            nuevo_registro = Union(opcion[1], nuevos_elementos)
            variantes[opcion[1]] = nuevo_registro


def crear_espacio_sin_reglas(array, resultado):
    array = array[::-1]

    while array:
        elemento = array.pop()
        counter = int(elemento.representacion)
        nombre = elemento.nombre
        if nombre in atomicos.keys() or nombre in variantes.keys():
            while counter:
                resultado.append(elemento)
                counter -= 1
        else:
                #for elem in elemento.elementos_optimo:
                #    if elem != 0:
                #        resultado.append(elemento)
                #    else:
                #        resultado.append(elem)
            resultado.append((elemento,elemento.elementos_optimo))
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
             
        if len(resultado) % alineacion == 0:
            if nombre in atomicos.keys() or nombre in variantes.keys():
                while counter:
                    resultado.append(elemento)
                    counter -= 1
            else:
               # for elem in elemento.elementos_optimo:
               #     if elem != 0:
               #         resultado.append(elemento)
               #     else:
               #         resultado.append(elem)
                resultado.append((elemento,elemento.elementos_optimo))
        else:
            while len(resultado) % alineacion != 0 :
                resultado.append(0)
            if nombre in atomicos.keys() or nombre in variantes.keys():
                while counter:
                    resultado.append(elemento)
                    counter -= 1
            else:
                #for elem in elemento.elementos_optimo:
                #    if elem != 0:
                #        resultado.append(elemento)
                #    else:
                #        resultado.append(elem)
                resultado.append((elemento,elemento.elementos_optimo))
                      
                
    #while len(resultado) % 4 != 0:
    #    resultado.append(0)
   # print(resultado)
   # split_array(resultado)
    return resultado

def verificar_hay_struct(array):
    resultado = []
    for elem in array:
        if elem.nombre in registros.keys():
            resultado.append(elem)
    return resultado

def verificar_hay_union(array):
    resultado = []
    for elem in array:
        if elem.nombre in variantes.keys():
            resultado.append(elem)
    return resultado


def determina_optimo(array):
    resultado = array[0]
    if(type(resultado) is tuple):
        resultado = resultado[1]
    
    for elem in array:
        try:
            numero = elem.count(0)
        except:
            numero = elem[1].count(0)
        if(numero < resultado.count(0)):
            if(type(elem) is tuple):
                resultado = elem[1]
            else:
                resultado = elem 
        
    return resultado, len(resultado)


def backtracking(nombre):
    resultado = []
    if nombre in registros.keys():
        arreglo = copy.deepcopy(registros[nombre].elementos)
        for lista in list(permutations(arreglo)):               
            webito = crear_espacio_con_reglas(list(lista), [])
            resultado.append(webito)
    
        return determina_optimo(resultado)
    
def gcd(a,b):
    while b:
        a,b = b, a%b
    return a

def lcm(a,b):
    return a*b // gcd(a,b)

def tamano_union(array):
    resultado = []
    for elem in array:
        resultado.append(int(elem.representacion))
    return max(resultado)

def alineacion_union(array):
    resultado = []
    for elem in array:
        resultado.append(int(elem.alineacion))
    return functools.reduce(lambda x, y: lcm(x, y), resultado)

def imprimir_array_como_matriz(array):
    
    for i in range(len(array)):
        if i % 4 == 0 : print()
        try:
            print(array[i].nombre + " |", end=" ")
        except:
            try:
                print(str(array[i][0].nombre) + " |", end =" ")
            except:
                print(str(array[i]) + " |", end =" ")
        

def print_sin_reglas(array, imprimir, interno, acumulado):
    indice = 0
    while indice < len(array):
        if(interno):
                print("\t", end="")
        if array[indice].nombre in atomicos.keys():
            print("Me encuentro en la posicion {}, {}".format(indice+acumulado, array[indice]))
            indice += int(array[indice].representacion)

        elif array[indice].nombre in registros.keys():
            print("Soy un struct, empiezo en la posicion {}, ocupo {} bytes".format(indice+acumulado, array[indice].representacion ))
            
            print_sin_reglas(array[indice].elementos_optimo, False, True, indice)
            indice += int(array[indice].representacion)
        elif array[indice].nombre in variantes.keys():
            print("Soy un union, empiezo en la posicion {}, ocupo {} bytes".format(indice+acumulado, array[indice].representacion))
            indice += int(array[indice].representacion)
    if imprimir:
        imprimir_array_como_matriz(array)

def struct_interno(array, struct, indice_inicial):
    indice = 0
    print("Soy un struct interno, empiezo en la posicion {}".format(indice_inicial))
    while indice < len(array):
        if(array[indice] == 0):
            indice += 1
            continue
        print("\t", end="")
        print("Me encuentro en la posicion {} del struct interno, {}".format(indice, array[indice]))
        indice += int(array[indice].representacion)
    print("Representacion del interno struct interno: ")
    imprimir_array_como_matriz(struct.elementos_optimo)
    print("\n---------------------------------------------------------")


def print_con_reglas(array, acumulado):
    indice = 0
    while indice < len(array):
        if (array[indice] == 0):
            indice +=1
            continue

        if(type(array[indice]) is tuple):
            struct_interno(array[indice][1], array[indice][0] ,indice)
            indice += 1
        
        elif array[indice].nombre in atomicos.keys():
            print("Me encuentro en la posicion {}, {}".format(indice, array[indice]))
            indice += int(array[indice].representacion)
  
        elif array[indice].nombre in variantes.keys():
            print("Soy un union, empiezo en la posicion {}, ocupo {} bytes".format(indice+acumulado, array[indice].representacion))
            indice += int(array[indice].representacion)
    
    imprimir_array_como_matriz(array)
def imprimir_variantes(variante):
    print("Soy un registro variante, mi tamano es de: {} bytes, y mi alineacion en caso de estar en un struct seria {}".format(variante.representacion, variante.alineacion))
    print("Mis posibles opciones son:")

    for elem in variante.elementos:
        print("\n")
        if type(elem) is Atomico:
            print("\t"+str(elem), end="")
        elif type(elem) is Union:
            print("\tSoy un registro variante interno, mi tamano es de: {} bytes, y mi alineacion en caso de estar en un struct seria {}".format(elem.representacion, elem.alineacion), end="")
        elif type(elem) is Struct:
            print("\tSoy un registro interno, mi tamano es de: {} bytes, y mi alineacion en caso de estar en un struct seria {}. Bytes desperdiciados en mi: {}".format(elem.representacion, elem.alineacion, elem.elementos_optimo.count(0)), end="")
            print("\tMi representacion seria la siguiente:")
            imprimir_array_como_matriz(elem.elementos_optimo)

def contar_perdida(array):
    resultado = array.count(0)
    cantidad = 0
    largo = len(array)
    listas = [x for x in array if type(x) is tuple]
    for lista in listas:
        cantidad += 1
        largo += len(lista[1])
        resultado += lista[1].count(0)

    return  largo-cantidad,resultado

def describir(nombre):
    
    if nombre in atomicos.keys():
        print(atomicos[nombre])

    elif nombre in registros.keys():
        
        #Tomamos todos los elementos
        a_evaluar = registros[nombre].elementos       
        structs = verificar_hay_struct(a_evaluar)
        unions = verificar_hay_union(a_evaluar)
        print("-------------------------------------------CASO STRUCT EMPAQUETADO--------------------------------------")
        #Caso Struct sin reglas
        if(structs):
            for elem in structs:
                elem.elementos_optimo = crear_espacio_sin_reglas(elem.elementos, []) 
                elem.representacion = len(elem.elementos_optimo)
        if(unions):
            for elem in unions:
                elem.representacion = tamano_union(elem.elementos)
        
        registros[nombre].elementos_optimo = crear_espacio_sin_reglas(a_evaluar, [])
        print_con_reglas(registros[nombre].elementos_optimo, 0)
        registros[nombre].representacion, registros[nombre].desperdicio = contar_perdida(registros[nombre].elementos_optimo)
        print("\nPara el caso empaquetado hubo un total de {} bytes ocupados, y una perdida de 0 bytes".format(registros[nombre].representacion))
        print()
        print("-------------------------------------------CASO STRUCT NO EMPAQUETADO--------------------------------------")
        #Caso Struct con reglas
        if(structs):
            for elem in structs:
                elem.elementos_optimo  = crear_espacio_con_reglas(elem.elementos, [])   
                elem.representacion = len(elem.elementos_optimo)        
                elem.alineacion = elem.elementos[0].alineacion

        if(unions):
            for elem in unions:
                elem.representacion = tamano_union(elem.elementos)
                elem.alineacion = alineacion_union(elem.elementos)

        registros[nombre].elementos_optimo = crear_espacio_con_reglas(a_evaluar, [])
        registros[nombre].representacion = len(registros[nombre].elementos_optimo)
        print_con_reglas(registros[nombre].elementos_optimo,  0)
        registros[nombre].representacion, registros[nombre].desperdicio = contar_perdida(registros[nombre].elementos_optimo)
        print("\nPara el caso no empaquetado hubo un total de {} bytes ocupados, y una perdida total de {} bytes".format(registros[nombre].representacion,registros[nombre].desperdicio))
        print()
        print("-------------------------------------------CASO STRUCT OPTIMIZACION--------------------------------------")
        #Caso Optimizacion
        if(structs):
            for elem in structs:
                elem.elementos_optimo,elem.representacion  = backtracking(elem.nombre)              
                elem.alineacion = elem.elementos_optimo[0].alineacion
        if(unions):
            for elem in unions:
                elem.representacion = tamano_union(elem.elementos)
                elem.alineacion = alineacion_union(elem.elementos)
        registros[nombre].elementos_optimo, registros[nombre].representacion = backtracking(nombre)
        print_con_reglas(registros[nombre].elementos_optimo,  0)
        registros[nombre].representacion, registros[nombre].desperdicio = contar_perdida(registros[nombre].elementos_optimo)
        print("\nPara el caso optimizado hubo un total de {} bytes ocupados, y una perdida total de {} bytes".format(registros[nombre].representacion,registros[nombre].desperdicio))
        print()
    elif nombre in variantes.keys():
        a_evaluar = variantes[nombre].elementos       
        structs = verificar_hay_struct(a_evaluar)
        unions = verificar_hay_union(a_evaluar)
        if(unions):
            for elem in unions:
                elem.representacion = tamano_union(elem.elementos)
                elem.alineacion = alineacion_union(elem.elementos)
        if(not(structs)):
            ###############################UNICO CASO#############################################
            variantes[nombre].representacion = tamano_union(variantes[nombre].elementos)
            variantes[nombre].alineacion = alineacion_union(variantes[nombre].elementos)
            imprimir_variantes(variantes[nombre])
        else:
            for elem in structs:
                elem.elementos_optimo = crear_espacio_sin_reglas(elem.elementos, []) 
                elem.representacion = len(elem.elementos_optimo)
            print("-------------------------------------------CASO UNION EMPAQUETADO--------------------------------------")
            print("\n")
            variantes[nombre].representacion = tamano_union(variantes[nombre].elementos)
            #variantes[nombre].alineacion = alineacion_union(variantes[nombre].elementos)
            imprimir_variantes(variantes[nombre])
            print("\n")
            print("-------------------------------------------CASO UNION NO EMPAQUETADO--------------------------------------")
            print("\n")
            for elem in structs:
                elem.elementos_optimo  = crear_espacio_con_reglas(elem.elementos, [])   
                elem.representacion = len(elem.elementos_optimo)        
                elem.alineacion = elem.elementos[0].alineacion

            variantes[nombre].representacion = tamano_union(variantes[nombre].elementos)
            variantes[nombre].alineacion = alineacion_union(variantes[nombre].elementos)
            imprimir_variantes(variantes[nombre])
            print("\n")
            print("-------------------------------------------CASO UNION OPTIMIZACION--------------------------------------")
            print("\n")
            for elem in structs:
                elem.elementos_optimo,elem.representacion  = backtracking(elem.nombre)              
                elem.alineacion = elem.elementos_optimo[0].alineacion
            
            variantes[nombre].representacion = tamano_union(variantes[nombre].elementos)
            variantes[nombre].alineacion = alineacion_union(variantes[nombre].elementos)
            imprimir_variantes(variantes[nombre])
            
      

def main():
    print("Bienvenido, por favor introduzca una de las opciones")
    opcion = ""
    while True:
        print("Introduzca ATOMICO <nombre> <representacion> <alineacion> para crear un nuevo tipo atomico")
        print("Introduzca STRUCT <nombre> [<tipo>] para crear un nuevo struct")
        print("Introduzca UNION <nombre> [<tipo>] para crear un nuevo struct")
        print("Introduzca DESCRIBIR <nombre> para describir un registro ya existente")
        print()
        opcion = input()
        if(es_valida(opcion)):
            opcion = opcion.split(" ")

            if(opcion[0].lower() == "atomico"):                
                crear_atomico(opcion)
                
            elif(opcion[0].lower() == "struct"):
                crear_registro(opcion, "struct")
               # print_structs()
            elif(opcion[0].lower() == "union"):
                crear_registro(opcion, "union")
            elif(opcion[0].lower() == "describir"):
                describir(opcion[1])
              
            elif(opcion[0].lower() == "salir"):
                break
        else:
            print("Por favor introduzca una opcion valida")
        print()

if __name__ == '__main__':
    main()