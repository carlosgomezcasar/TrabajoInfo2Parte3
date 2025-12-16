class NodoHistorial:
    def __init__(self, dato, anterior=None, siguiente=None):
        self.dato = dato
        self.anterior = anterior
        self.siguiente = siguiente


class HistorialEstados:
    """Lista doblemente enlazada con puntero 'actual' para gestionar
    deshacer/rehacer estados de la biblioteca.
    """
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.actual = None
        self.size = 0

    def esta_vacio(self):
        return self.primero is None

    def inicializar_con_estado(self, estado):
        """Inicializa el historial con un único estado (por ejemplo, el estado
        justo tras la sincronización inicial con el servidor).
        Borra cualquier cosa anterior que pudiera haber.
        """
        nodo = NodoHistorial(estado)
        self.primero = nodo
        self.ultimo = nodo
        self.actual = nodo
        self.size = 1

    def _eliminar_nodos_despues_de(self, nodo):
        """Elimina todos los nodos que vienen después de 'nodo' (hacia la derecha).
        Deja 'nodo' como último de la lista.
        """
        actual = nodo.siguiente
        while actual is not None:
            siguiente = actual.siguiente
            actual.anterior = None
            actual.siguiente = None
            actual = siguiente

        nodo.siguiente = None
        self.ultimo = nodo
        self._recalcular_num_nodos()

    def _recalcular_num_nodos(self):
        """Recuenta el número de nodos de la lista."""
        contador = 0
        actual = self.primero
        while actual is not None:
            contador += 1
            actual = actual.siguiente
        self.size = contador

    def registrar_nuevo_estado(self, estado):
        """Registra un nuevo estado de la biblioteca tras una modificación.
        - Si hay estados 'futuros' (actual no es el último), se eliminan.
        - Se inserta el nuevo estado al final.
        - El puntero 'actual' pasa a ese nuevo nodo.
        """
        if self.esta_vacio():
            # Si no hay estados, inicializamos
            self.inicializar_con_estado(estado)
            return

        # Si actual no es el último, hay estados "rehacibles": los eliminamos
        if self.actual is not self.ultimo:
            self._eliminar_nodos_despues_de(self.actual)

        # Insertar un nuevo nodo al final
        nuevo = NodoHistorial(estado, anterior=self.ultimo, siguiente=None)
        self.ultimo.siguiente = nuevo
        self.ultimo = nuevo
        self.actual = nuevo
        self.size += 1

    def puede_deshacer(self):
        """Devuelve True si hay un estado anterior al actual."""
        return self.actual is not None and self.actual.anterior is not None

    def puede_rehacer(self):
        """Devuelve True si hay un estado posterior al actual."""
        return self.actual is not None and self.actual.siguiente is not None

    def deshacer(self):
        """Mueve el puntero actual una posición hacia atrás y devuelve el estado.
        Lanza IndexError si no se puede deshacer.
        """
        if not self.puede_deshacer():
            raise IndexError("No se puede deshacer: no hay estado anterior")

        self.actual = self.actual.anterior
        return self.actual.dato

    def rehacer(self):
        """Mueve el puntero actual una posición hacia adelante y devuelve el estado.
        Lanza IndexError si no se puede rehacer.
        """
        if not self.puede_rehacer():
            raise IndexError("No se puede rehacer: no hay estado posterior")

        self.actual = self.actual.siguiente
        return self.actual.dato

    def obtener_estado_actual(self):
        """Devuelve el estado almacenado en el nodo actual."""
        if self.actual is None:
            return None
        return self.actual.dato

    def __len__(self):
        """Permite usar len(historial)."""
        return self.size
