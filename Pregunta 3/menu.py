from registros import *

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