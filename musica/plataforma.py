from musica.cancion import Cancion
from musica.lista_reproduccion import ListaReproduccion
from typing import List


class PlataformaMusical:

    def __init__(self):
        self.canciones: List[Cancion] = []
        self.listas: List[ListaReproduccion] = []

    def registrar_cancion(self, titulo: str, artista: str, duracion: int, genero: str, archivo: str) -> bool:
        """
        Registra una nueva canción en la plataforma.
        - Si ya existe una canción con el mismo título y artista, no la añade y devuelve False.
        - Asigna un id autoincremental (1 + max id existente, o 1 si no hay canciones).
        - Devuelve True si la canción se añadió correctamente.
        """
        # Comprueba duplicados por título y artista
        for c in self.canciones:
            if c.titulo == titulo and c.artista == artista:
                # No añadimos duplicados
                return False

        # Calcular id autoincremental
        next_id = 1
        if self.canciones:
            max_id = max((c.id for c in self.canciones), default=0)
            next_id = max_id + 1

        nueva = Cancion(next_id, titulo, artista, duracion, genero, archivo)
        self.canciones.append(nueva)
        return True

    def editar_cancion(self, id: int, titulo: str, artista: str, duracion: int, genero: str, archivo: str) -> bool:
        """
        Edita una canción existente en la plataforma.
        Devuelve True si se modifica correctamente, False si no existe una canción con ese id.
        """
        # Buscar la canción por su ID
        for c in self.canciones:
            if c.id == id:
                # Actualizar sus atributos
                c.titulo = titulo
                c.artista = artista
                c.duracion = duracion
                c.genero = genero
                c.archivo_mp3 = archivo
                return True

        # Si no se encontró ninguna canción con ese ID
        return False

    def eliminar_cancion(self, id: int) -> bool:
        """
        Elimina una canción de la plataforma.
        - Si no existe, devuelve False.
        - Si existe, la elimina de self.canciones y de todas las listas de reproducción, y devuelve True.
        """
        # Buscar la canción por id
        for c in self.canciones:
            if c.id == id:
                self.canciones.remove(c)

                # También eliminar de todas las listas de reproducción donde aparezca
                for lista in self.listas:
                    if id in lista.canciones:
                        lista.canciones.remove(id)

                return True

        # Si no se encuentra la canción
        return False

    def crear_lista(self, nombre: str) -> bool:
        """
        Crea una nueva lista de reproducción.
        - Si ya existe una lista con el mismo nombre (sin importar mayúsculas), devuelve False.
        - Si se crea correctamente, devuelve True.
        """
        # Comprobar si ya existe una lista con el mismo nombre
        for lista in self.listas:
            if lista.nombre.lower() == nombre.lower():
                return False

        nueva_lista = ListaReproduccion(nombre)
        self.listas.append(nueva_lista)
        return True

    def borrar_lista(self, nombre: str) -> bool:
        """
        Elimina una lista de reproducción por nombre.
        - Si existe una lista con ese nombre (sin importar mayúsculas), la elimina y devuelve True.
        - Si no existe ninguna lista con ese nombre, devuelve False.
        """
        for lista in self.listas:
            if lista.nombre.lower() == nombre.lower():
                self.listas.remove(lista)
                return True
        return False

    def obtener_lista(self, nombre: str) -> ListaReproduccion | None:
        """
        Devuelve una lista de reproducción existente por su nombre.
        - Si existe, devuelve el objeto ListaReproduccion correspondiente.
        - Si no existe, devuelve None.
        - La comparación de nombres no distingue mayúsculas/minúsculas.
        """
        for lista in self.listas:
            if lista.nombre.lower() == nombre.lower():
                return lista
        return None


    # MÉTODOS PARA LA SERIALIZACIÓN

    def to_dict(self) -> dict:
        """
        Convierte toda la plataforma en un diccionario serializable:
        - canciones: lista de dicts
        - listas: lista de dicts
        """
        return {
            "canciones": [c.to_dict() for c in self.canciones],
            "listas": [l.to_dict() for l in self.listas],
        }

    def from_dict(data: dict, base_path: str) -> "PlataformaMusical":
        """
        Crea una PlataformaMusical a partir de un diccionario.
        base_path es la carpeta local donde están (o estarán) los mp3 del usuario.
        """
        p = PlataformaMusical()

        # Reconstruir canciones
        for cdata in data.get("canciones", []):
            p.canciones.append(Cancion.from_dict(cdata, base_path))

        # Reconstruir listas
        for ldata in data.get("listas", []):
            p.listas.append(ListaReproduccion.from_dict(ldata))

        return p