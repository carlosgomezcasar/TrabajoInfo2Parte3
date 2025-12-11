# pila.py

class NodoPila:
    """Nodo para la pila enlazada."""

    def __init__(self, dato, siguiente=None):
        self.dato = dato          # Lo que guardamos (por ejemplo, ruta del JSON)
        self.siguiente = siguiente  # Referencia al siguiente nodo (el de abajo en la pila)


class Pila:
    """Implementación de una pila LIFO usando nodos enlazados.
    Operaciones principales: apilar (push), desapilar (pop), cima (peek).
    """

    def __init__(self):
        self.tope = None          # Nodo que está arriba del todo
        self._num_elementos = 0   # Contador de elementos (opcional, pero útil)

    def esta_vacia(self):
        """Devuelve True si la pila no tiene elementos."""
        return self.tope is None

    def apilar(self, dato):
        """Inserta un nuevo elemento en la parte superior de la pila."""
        nuevo_nodo = NodoPila(dato, self.tope)
        self.tope = nuevo_nodo
        self._num_elementos += 1

    def desapilar(self):
        """Elimina y devuelve el elemento superior de la pila.
        Lanza IndexError si la pila está vacía.
        """
        if self.esta_vacia():
            raise IndexError("No se puede desapilar: la pila está vacía")

        dato = self.tope.dato
        self.tope = self.tope.siguiente
        self._num_elementos -= 1
        return dato

    def cima(self):
        """Devuelve el elemento superior de la pila sin eliminarlo.
        Lanza IndexError si la pila está vacía.
        """
        if self.esta_vacia():
            raise IndexError("No se puede acceder a la cima: la pila está vacía")

        return self.tope.dato

    def __len__(self):
        """Permite usar len(pila)."""
        return self._num_elementos
