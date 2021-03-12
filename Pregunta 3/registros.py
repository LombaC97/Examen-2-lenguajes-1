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
   
    if opcion[0].lower() != "atomico" and opcion[0].lower() != "struct" and opcion[0].lower != "describir":        
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

        registros[opcion[1]] = nuevos_atomicos

def describir(nombre):
    jk


def main():
    print("Bienvenido, por favor introduzca una de las opciones")
    opcion = ""
    while True:
        print("Introduzca ATOMICO <nombre> <representacion> <alineacion> para crear un nuevo tipo atomico")
        print("Introduzca STRUCT <nombre> [<tipo>] para crear un nuevo struct")
        opcion = input()
        if(es_valida(opcion)):
            opcion = opcion.split(" ")

            if(opcion[0].lower() == "atomico"):                
                crear_atomico(opcion)
                print_atomicos()
            elif(opcion[0].lower() == "struct"):
                crear_registro(opcion)
                print_structs()
            elif(opcion[0].lower() == "salir"):
                break
        else:
            print("Por favor introduzca una opcion valida")

   



if __name__ == '__main__':
    main()