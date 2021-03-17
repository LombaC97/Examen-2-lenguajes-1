package main

import "fmt"

//El tipo function puede ser una interfaz vacia
//O una funcion que recibe una interfaz vacia
type function func(interface{}) interface{}

//Se representan los numerales de church
// como un function o una funcion que recibe un function
type Church func(function) function

//El cero es basicamente retornar una funcion que retorna
// una interfaz vacia y una function(definida mas arriba)
// Dicha function lo que hace es retornar x que es la function vacia
func cero(fun function) function {
	return func(x interface{}) interface{} {
		return x
	}
}

//Para el sucesor recibimos un numero de church y devolvemos
// un numero de church
func (a Church) sucesor() Church {
	return func(fun function) function {
		return func(x interface{}) interface{} {
			return fun(a(fun)(x))
		}
	}
}

//Implementamos un metodo sobre Church para la suma
func (a Church) sumar(b Church) Church {
	return func(fun function) function {
		return func(x interface{}) interface{} {
			return a(fun)(b(fun)(x))
		}
	}
}

//Implementamos un metodo sobre Church para la Multiplicacion
func (a Church) multiplicar(b Church) Church {
	return func(fun function) function {
		return func(x interface{}) interface{} {
			return a(b(fun))(x)
		}
	}
}

//Para poder verlos como enteros
func (a Church) toInt() int {
	return a(incr)(0).(int)
}
func incr(i interface{}) interface{} {
	return i.(int) + 1
}

func main() {
	c := Church(cero)
	//Para crear los numeros simplemente aplicamos sucesor a z tantas veces como querramos para obtenerlo
	cuatro := c.sucesor().sucesor().sucesor().sucesor()
	nueve := c.sucesor().sucesor().sucesor().sucesor().sucesor().sucesor().sucesor().sucesor().sucesor()

	fmt.Println("nueve + cuatro =", nueve.sumar(cuatro).toInt())
	fmt.Println("nueve * cuatro =", nueve.multiplicar(cuatro).toInt())

}
