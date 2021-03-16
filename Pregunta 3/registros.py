#Carlos Gonzalez
#Carnet: 15-10611

import copy
import functools
from itertools import permutations
class Atomico:
    def __init__(self,nombre, representacion, alineacion):
        self.nombre = nombre
        self.representacion = representacion
        self.alineacion = alineacion

    def __str__(self):
        return "Soy un registro atomico de nombre: {}, mi representacion es de {} bytes y mi alineacion es de {} bytes".format(self.nombre,self.representacion, self.alineacion)
#Clase Struct que tendra nombre, alineacion, representacion, etc
class Struct:
    def __init__(self, nombre, elementos, representacion= None, alineacion = None, elementos_optimo = None, desperdicio = None):
        self.nombre = nombre
        self.elementos = elementos
        self.representacion = representacion
        self.alineacion = alineacion
        self.desperdicio = desperdicio
        self.elementos_optimo = elementos_optimo
#Clase union que tendra igualmente nombre, representacion, alineacion
class Union:
    def __init__(self, nombre, elementos, representacion = None, alineacion = None):
        self.nombre = nombre
        self.elementos = elementos
        self.representacion = representacion
        self.alineacion = alineacion

#Tendremos 3 diccionarios donde se guardaran todos los distintos elementos que creemos. Esto para poder acceder a cada uno rapidamente
atomicos = dict()
registros = dict()
variantes = dict()

#Funcion que verifica si el nombre que desea introducir el usuario ya existe en algun diccionario
def ya_existente(opcion):
    if ( opcion[1] in atomicos.keys() or opcion[1] in registros.keys() or opcion[1] in variantes.keys() ):
        print("Nombre ya existente") 
        return True 
# Funcion que crea un atomico con clave (nombre introducido por el usuario) y valor Atomico(nombre, representacion, alineacion)
def crear_atomico(opcion):
    if(not(ya_existente(opcion))):          
        atomicos[opcion[1]] = Atomico(opcion[1],opcion[2], opcion[3])
#Funcion que verifica el nivel de anidamiento    
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
#Funcion que crea structs o crea unions, basicamente
def crear_registro(opcion, tipo):
    
    if not(ya_existente(opcion)): 
        for elem in opcion[2:]: 
            if elem not in atomicos.keys() and elem not in registros.keys() and elem not in variantes.keys():
                print("Ha introducido un tipo no existente")
                return
        if (nivel_anidamiento(opcion)):
            return print("Excedido el maximo nivel de anidamiento permitido")
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

#Funcion utilizada para crear el espacio sin ninguna regla
def crear_espacio_sin_reglas(array, resultado):
    #Invertimos el array (ya que utilizaremos .pop)
    array = array[::-1]
    #Mientras que el array exista
    while array:
        elemento = array.pop()
        counter = int(elemento.representacion)
        nombre = elemento.nombre
        # Si es un atomico o un variante, simplemente introducimos el elemento en el nuevo espacio
        # tantas veces como su representacion lo indice (el counter es la representacions)
        if nombre in atomicos.keys() or nombre in variantes.keys():
            while counter:
                resultado.append(elemento)
                counter -= 1
        #En caso de que sea struct, hace append de una tupla con el elemento y el array de elementos optimo
        # de ese Struct (en este caso el elementos_optimo es poner una cosa al lado de la otra sin reglas de alineacion)
        else:             
            resultado.append((elemento,elemento.elementos_optimo))
            
    return resultado
  
#Funcion utilizada para crear espacio respetando reglas de alineamiento
def crear_espacio_con_reglas(array, resultado):
    
    array = array[::-1]
    
    while array:
        elemento = array.pop()
        counter = int(elemento.representacion)
        alineacion = int(elemento.alineacion)
        nombre = elemento.nombre 
        #Verificamos esta condicion para saber si ya podemos introducir el elemento en el array (hacer append)
        if len(resultado) % alineacion == 0:
            if nombre in atomicos.keys() or nombre in variantes.keys():
                while counter:
                    resultado.append(elemento)
                    counter -= 1
            else:
               
                resultado.append((elemento,elemento.elementos_optimo))
        else:
            #Si no tiene el len apropiado todavia, entonces rellenamos con 0 (que son espacios desperdiciados)
            #hasta que el len sea el adecuado segun su alineacion
            while len(resultado) % alineacion != 0 :
                resultado.append(0)
            if nombre in atomicos.keys() or nombre in variantes.keys():
                while counter:
                    resultado.append(elemento)
                    counter -= 1
            else:
             
                resultado.append((elemento,elemento.elementos_optimo))
                      
    return resultado
#Funcion utilizada para verificar si hay algun struct dentro de un array 
def verificar_hay_struct(array):
    resultado = []
    for elem in array:
        if elem.nombre in registros.keys():
            resultado.append(elem)
    return resultado
#Funcion utilizada para verificar si hay un registro variante dentro de un array
def verificar_hay_union(array):
    resultado = []
    for elem in array:
        if elem.nombre in variantes.keys():
            resultado.append(elem)
    return resultado

#Funcion que, determina dentro de un array, cuantos 0's hay (o sea, espacios vacios)
#Y busca aquella que tenga la menor cantidad de 0's posibles y la retorna
def determina_optimo(array):
    nousar, minimo = contar_perdida(array[0])
    resultado = array[0]

    for lista in array:        
        largo, perdida = contar_perdida(lista)
        if(perdida < minimo):
            minimo = perdida
            resultado = lista
    return resultado, len(resultado)


#Funcion utilizada para buscar el mejor caso que respete la alineacion y pierda la menor cantidad de 
#bytes posible
def optimizacion(nombre):
    resultado = []
    if nombre in registros.keys():
        arreglo = copy.deepcopy(registros[nombre].elementos)
        #list(perumations(arreglo)) tiene todas las permutaciones posibles del array de entrada.
        #El array de entrada son todos los elementos que tiene dicho struct
        for lista in list(permutations(arreglo)):
            #Por cada posible permutacion creamos una variacion distinta cumplieando las posibles alineaciones               
            resultado.append(crear_espacio_con_reglas(list(lista), []))
        #Creamos un array de arrays, y lo pasamos a la funcion determina_optimo, para ver cual de ellas es la que tiene mejor
        #optimizacion y menor pérdida
        return determina_optimo(resultado)
#Funcion para determinar el maximo comun divisor de dos numeros
def gcd(a,b):
    while b:
        a,b = b, a%b
    return a
#Funcion para determinar el minimo comun multimo entre dos numeros
def lcm(a,b):
    return a*b // gcd(a,b)

#Funcion utilizada por los union, basicamente busca entre todas las representaciones de sus posibles elementos
# y selecciona aquella que sea mayor
def tamano_union(array):
    resultado = []
    for elem in array:
        resultado.append(int(elem.representacion))
    return max(resultado)
#Funcion utilizada por los union, basicamente busca entre las alineaciones de todos sus posibles elementos
#Y retorna el minimo comun multiplo entre todos ellos
def alineacion_union(array):
    resultado = []
    for elem in array:
        resultado.append(int(elem.alineacion))
    return functools.reduce(lambda x, y: lcm(x, y), resultado)
#Funcion utilizada para imprimir un array como una matriz, diviendolo de 4 en 4
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
        
#Funcion utilizada para hacer print de un struct interno
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

#Funcion utilizada para imprimir los elementos de un struct
def print_struct(array, acumulado):
    indice = 0
    while indice < len(array):
        if (array[indice] == 0):
            indice +=1
            continue
        #Si el elemento es una tupla, quiere decir que previamente en crear_espacio_con_reglas vimos que era un struct
        #e hicimos un .append de (el elemento, los .elementos_optimo del struct)
        if(type(array[indice]) is tuple):
            struct_interno(array[indice][1], array[indice][0] ,indice)
            indice += 1
        
        elif array[indice].nombre in atomicos.keys():
            print("Me encuentro en la posicion {}, {}".format(indice, array[indice]))
            indice += int(array[indice].representacion)
  
        elif array[indice].nombre in variantes.keys():
            print("Soy un union, empiezo en la posicion {}, ocupo {} bytes, mi alineacion es {}".format(indice+acumulado, array[indice].representacion, array[indice].alineacion))
            indice += int(array[indice].representacion)
    
    imprimir_array_como_matriz(array)

#Funcion utilizada para imprimir registros variantes
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
            print("\t Mi representacion (struct interno) seria la siguiente:")
            imprimir_array_como_matriz(elem.elementos_optimo)

#Funcion para contar todas las posibles perdidas de un struct dentro de otro, basicamente
#toma todas estas perdidas en consideracion y devuelve el len del array y el resultado que es la cantidad
#total de bytes perdidos que existen en la lista, y en las tuplas dentro de esa lista
def contar_perdida(array):
    resultado = array.count(0)
    cantidad = 0
    largo = len(array)
    listas = [x for x in array if type(x) is tuple]
    for lista in listas:
        cantidad += 1
        largo += len(lista[1])
        resultado += lista[1].count(0)

    return  largo-cantidad, resultado

#Funcion utilizada para describir un elemento
#Notese que elementos_optimo es un atributo que contiene su representacion dependiendo de cada caso,
#Es decir, empaquetado, no empaquetado y optimizado previamente (reordenado)
def describir(nombre):
    #Si es un atomico, imprimimos sus caracteristicas
    if nombre in atomicos.keys():
        print(atomicos[nombre])
        return str(atomicos[nombre])
    #Si es un struct
    elif nombre in registros.keys():
       
        #Tomamos todos los elementos que puede tener ese struct 
        a_evaluar = registros[nombre].elementos  
        #Vemos si tiene structs internos     
        structs = verificar_hay_struct(a_evaluar)
        #Vemos si tiene unions internos
        unions = verificar_hay_union(a_evaluar)
        
        print("-------------------------------------------CASO STRUCT EMPAQUETADO--------------------------------------")
        #Caso Struct sin reglas
        if(structs):
            for elem in structs:
                #A cada struct interno lo procesamos primero, y asignamos en su .elementos_optimo dependiendo del caso.
                #En este caso, creamos su espacio sin reglas de alineacion primero
                elem.elementos_optimo = crear_espacio_sin_reglas(elem.elementos, []) 
                #Y determinamos su representacion
                elem.representacion = len(elem.elementos_optimo)
        if(unions):
            for elem in unions:
                #Determinamos el tamano de los unions utilizando la funcion previamente mencionada
                elem.representacion = tamano_union(elem.elementos)
        
        #Una vez procesados sus structs internos y unions internos (de haberlos) procesamos al externo (que los contiene)
        #Llamamos a la misma funcion para crear espacio sin reglas y determinamos su elementos_optimo
        # En este caso, elementos_optimo no es el optimo, sino el que corresponde a su espacio sin reglas de alineacion
        registros[nombre].elementos_optimo = crear_espacio_sin_reglas(a_evaluar, [])
        #Imprimimos
        print_struct(registros[nombre].elementos_optimo, 0)
        #Calculamos la representacion y desperdicio
        registros[nombre].representacion, registros[nombre].desperdicio = contar_perdida(registros[nombre].elementos_optimo)
        print("\nPara el caso empaquetado hubo un total de {} bytes ocupados, y una perdida de 0 bytes".format(registros[nombre].representacion))
        print()
        print("-------------------------------------------CASO STRUCT NO EMPAQUETADO--------------------------------------")
        #Caso Struct con reglas
        #Repetimos lo mismo para el caso no empaquetado
        if(structs):
            for elem in structs:
                #Creamos para los structs internos su espacio con reglas
                elem.elementos_optimo  = crear_espacio_con_reglas(elem.elementos, [])   
                elem.representacion = len(elem.elementos_optimo)
                #La diferencia es que ahora si me importa la alineacion, como es el caso no empaquetado,
                #puedo saber que su alineacion va a ser la misma que si primer elemento
                elem.alineacion = elem.elementos[0].alineacion

        if(unions):
            for elem in unions:
                elem.representacion = tamano_union(elem.elementos)
                #Determinamos ahora la alineacion del registro variante
                elem.alineacion = alineacion_union(elem.elementos)
        #Y ahora creamos el espacio para el struct externo y guardamos su elementos_optimo
        #En este caso, el elementos optimo no es el optimo, sino como quedaria en el caso empaquetado
        #(se guardan los campos en el mismo orden en que fueron declaradoss)
        registros[nombre].elementos_optimo = crear_espacio_con_reglas(a_evaluar, [])
        
        registros[nombre].representacion = len(registros[nombre].elementos_optimo)
        #Imprimimos ahora este struct externo ya teniendo todos los elementos necesarios
        print_struct(registros[nombre].elementos_optimo,  0)
        #Y ahora determinamos cual fue su tamano total (incluyendo el tamano de los structs internos) y el desperdicio total
        registros[nombre].representacion, registros[nombre].desperdicio = contar_perdida(registros[nombre].elementos_optimo)
        print("\nPara el caso no empaquetado hubo un total de {} bytes ocupados, y una perdida total de {} bytes".format(registros[nombre].representacion, registros[nombre].desperdicio))
        print()
        print("-------------------------------------------CASO STRUCT OPTIMIZACION--------------------------------------")
        #Caso Optimizacion
        if(structs):
            for elem in structs:
                #Optimizamos primero a los structs internos
                elem.elementos_optimo,elem.representacion  = optimizacion(elem.nombre) 
                #Como ahora no es el primer registro, la alineacion del struct interno va a depender del primer elemento
                #que haya quedado en su caso optimo             
                elem.alineacion = elem.elementos_optimo[0].alineacion
        if(unions):
            for elem in unions:
                #Similar al caso de los unions anterior
                elem.representacion = tamano_union(elem.elementos)
                elem.alineacion = alineacion_union(elem.elementos)
        #Una vez que ya optimizamos a todos los registros internos, entonces optimizamos al registro
        #exterior
        registros[nombre].elementos_optimo, registros[nombre].representacion = optimizacion(nombre)
        #Imprimimos
        print_struct(registros[nombre].elementos_optimo,  0)
        #Determinamos tamano y perdida
        registros[nombre].representacion, registros[nombre].desperdicio = contar_perdida(registros[nombre].elementos_optimo)
        print("\nPara el caso optimizado hubo un total de {} bytes ocupados, y una perdida total de {} bytes".format(registros[nombre].representacion,registros[nombre].desperdicio))
        print()
    elif nombre in variantes.keys():
        #Muy similar al caso de los Structs
        a_evaluar = variantes[nombre].elementos       
        structs = verificar_hay_struct(a_evaluar)
        unions = verificar_hay_union(a_evaluar)
        if(unions):
            for elem in unions:
                #Si hay unions internos entonces determinamos alineacion y tamano
                elem.representacion = tamano_union(elem.elementos)
                elem.alineacion = alineacion_union(elem.elementos)
        if(not(structs)):
            #Si no hay structs, entonces imprimimos los elementos internos
            ###############################UNICO CASO#############################################
            variantes[nombre].representacion = tamano_union(variantes[nombre].elementos)
            variantes[nombre].alineacion = alineacion_union(variantes[nombre].elementos)
            imprimir_variantes(variantes[nombre])
        else:
            #En caso de que haya structs internos, entonces nuevamente estudiamos los tres casos
            #como pudiera variar el union: que el struct interno estuviera empaquetado, que el struct interno
            #estuviera no empaquetado y que el struct interno estuviera optimizado.
            #Se determina cada uno de manera similar al apartado anterior
            for elem in structs:
                elem.elementos_optimo = crear_espacio_sin_reglas(elem.elementos, []) 
                elem.representacion = len(elem.elementos_optimo)
            print("-------------------------------------------CASO UNION EMPAQUETADO--------------------------------------")
            print("\n")
            variantes[nombre].representacion = tamano_union(variantes[nombre].elementos)
            #Llamamos a la funcion para imprimir variantes
            imprimir_variantes(variantes[nombre])
            print("\n")
            print("-------------------------------------------CASO UNION NO EMPAQUETADO--------------------------------------")
            print("\n")
            for elem in structs:
                elem.elementos_optimo  = crear_espacio_con_reglas(elem.elementos, [])   
                elem.representacion = len(elem.elementos_optimo)        
                elem.alineacion = elem.elementos[0].alineacion
            #Luego de determinar el caso de los structs internos, entonces debemos determinar la representacion
            #y alineacion del union que lo contiene
            variantes[nombre].representacion = tamano_union(variantes[nombre].elementos)
            variantes[nombre].alineacion = alineacion_union(variantes[nombre].elementos)
            imprimir_variantes(variantes[nombre])
            print("\n")
            print("-------------------------------------------CASO UNION OPTIMIZACION--------------------------------------")
            print("\n")
            #Determinamos la manera optima del struct interno, optimizando espacio y respetando alineaciones
            for elem in structs:
                elem.elementos_optimo,elem.representacion  = optimizacion(elem.nombre)              
                elem.alineacion = elem.elementos_optimo[0].alineacion
            #Una vez que hayan sido determinados, entonces determinamos la representacion y alineacion del registro variante
            variantes[nombre].representacion = tamano_union(variantes[nombre].elementos)
            variantes[nombre].alineacion = alineacion_union(variantes[nombre].elementos)
            imprimir_variantes(variantes[nombre])
    else:
        print("Nombre no encontrado")
            