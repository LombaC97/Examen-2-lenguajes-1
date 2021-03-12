package main

import (
	"fmt"
	"math"
)

//Definimos el nodo, tendra un value int64 y
// un hijo derecho y un hijo izquierdo que son apuntadores a
//otros Node
type Node struct {
	value int64
	left  *Node
	right *Node
}

//El  Tree solamente tiene un atributo que es
//la raiz del arbol
type Tree struct {
	root *Node
}

//Definimos un metodo para el struct Tree que tendra
//Si el arbol es nulo (lo acabamos de crear) entonces
//Inserta el nodo en la raiz del arbol
//En cualquier otro caso, llama a la funcion de insercion
// de Node
func (t *Tree) insert(value int64) *Tree {
	if t.root == nil {
		t.root = &Node{value: value, left: nil, right: nil}
	} else {
		t.root.insert(value)
	}
	return t
}

// La funcion de insercion de Node inserta los nodos en orden
// de encadenamiento mas abajo. No cuida mantener el orden de
// que se trate de un Arbol de Busqueda binaria, solamente
// va construyendo un arbol binario cualquiera
func (n *Node) insert(value int64) {
	if n == nil {
		return
	} else if n.left == nil {
		n.left = &Node{value: value, left: nil, right: nil}
	} else if n.right == nil {
		n.right = &Node{value: value, left: nil, right: nil}
	} else {
		if n.left != nil {
			n.left.insert(value)
		} else {

			n.right.insert(value)
		}

	}
}

// La funcion print sencillamente imprime el arbol para poder
// Ver que es lo que se esta generando
func print(node *Node, tab int, quien string) {
	if node == nil {
		return
	}
	for i := 0; i < tab; i++ {
		fmt.Printf(" ")
	}
	fmt.Printf("%s %d\n", quien, node.value)

	print(node.left, tab+2, "Hijo Izquierdo")
	print(node.right, tab+2, "Hijo Derecho")
}

//Esta es la funcion que determina si un arbol binario es de
// busqueda.
func (node *Node) isBST(min, max int64) bool {
	//Si el nodo es nil, retorna true
	if node == nil {
		return true
	}
	//Si el .value del nodo actual es < al minimo
	//Entonces quiere decir que no es binario de busqueda
	if node.value < min {
		return false
	}
	//Asi mismo, si el .value del nodo actual es mayor al
	// maximo, entonces no es binario de busqueda
	if node.value > max {
		return false
	}
	//Llamamos recursivamente a la funcion con ambos hijos
	//Notemos que es en este momento donde hacemos cumplir la definicion
	// de Arbol binario de busqueda
	//Llamamos a su hijo derecho con el minimo seteado al valor del nodo
	//Actual (ya que el hijo derecho debe tener un valor mayor al valor del
	//nodo actual). Y lo mismo con el hijo izquierdo pero con el maximo
	return node.right.isBST(node.value, max) &&
		node.left.isBST(min, node.value)
}

func main() {
	//Creamos un arbol vacío
	tree := &Tree{}
	//Insertamos en dicho arbol encadenando los insert
	//Notese que el orden que se insertaran los nodos sera
	//el mismo en que se defina en estas llamadas a .insert
	//La primera llamada devuelve un arbol, y las llamadas subsiguientes
	//Llaman al insert de Node
	tree.insert(100).
		insert(20).
		insert(200).
		insert(20).
		insert(22)
	//Vemos si es un arbol binario de busqueda.
	//Los valores min y max iniciales son los permitidos dentro de
	//Int64
	busqueda := tree.root.isBST(math.MinInt64, math.MaxInt64)
	//Imprimirmos el arbol
	print(tree.root, 0, "Raiz")
	//Imprimimos el resultado de la funcion
	fmt.Println(busqueda)
}
