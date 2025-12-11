from typing import List

class ListaReproduccion:
    """
    Esta clase es una lista de reproducción, que va a tener
    su propio nombre, y dentro de ella sus canciones sin duplicados.
    Implementamos los métodos anadir_cancion y quitar_cancion.
    """

    def __init__(self, nombre: str):
        self.nombre: str = nombre
        self.canciones: List[int] = []

    def anadir_cancion(self, id_cancion: int) -> bool:
        """
        Añade el id de una canción si no estaba ya en la lista.
        Devuelve True si se añade, False si ya estaba.
        """
        if id_cancion not in self.canciones:
            self.canciones.append(id_cancion)
            return True
        return False

    def quitar_cancion(self, id_cancion: int) -> bool:
        """
        Quita el id de una canción si estaba en la lista.
        Devuelve True si se elimina, False si no estaba.
        """
        if id_cancion in self.canciones:
            self.canciones.remove(id_cancion)
            return True
        return False

    # MÉTODOS PARA LA SERIALIZACIÓN

    def to_dict(self) -> dict:
        """
        Convierte la lista de reproducción en un diccionario serializable.
        """
        return {
            "nombre": self.nombre,
            "canciones": self.canciones,  #lista de ids
        }

    def from_dict(data: dict) -> "ListaReproduccion":
        """
        Crea una ListaReproduccion a partir de un diccionario.
        """
        lista = ListaReproduccion(data["nombre"])
        lista.canciones = list(data.get("canciones", []))
        return lista