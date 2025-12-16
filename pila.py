class NodoPila:
    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente


class Pila:
    def __init__(self):
        self.cima = None
        self.size = 0

    def esta_vacia(self):
        return self.cima is None

    def apilar(self, dato):
        """Inserta un nuevo elemento en la parte superior de la pila."""
        nuevo_nodo = NodoPila(dato, self.cima)
        self.cima = nuevo_nodo
        self.size += 1

    def desapilar(self):
        """Elimina y devuelve el elemento superior de la pila."""
        if self.esta_vacia():
            raise IndexError("No se puede desapilar: la pila está vacía")

        dato = self.cima.dato
        self.cima = self.cima.siguiente
        self.size -= 1
        return dato

    def peek(self):
        """Devuelve el elemento superior de la pila sin eliminarlo."""
        if self.esta_vacia():
            raise IndexError("No se puede acceder a la cima: la pila está vacía")

        return self.cima.dato

    def __len__(self):
        """Permite usar len(pila)"""
        return self.size
