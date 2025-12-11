import pygame
import os

class Cancion:
    def __init__(self, id: int, titulo: str, artista: str, duracion: int, genero: str, archivo_mp3: str):
        self.id = id
        self.titulo = titulo
        self.artista = artista
        self.duracion = duracion
        self.genero = genero
        self.archivo_mp3 = archivo_mp3

    def reproducir(self) -> None:
        """
        Reproduce la canción.
        Usa pygame.mixer para reproducir el archivo MP3.
        """
        if not os.path.exists(self.archivo_mp3):
            print(f'No se encontró el archivo: {self.archivo_mp3}')
            return

        # Si pygame no está inicializado, se inicializa una sola vez
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Al reproducir una nueva canción, pygame detiene automáticamente la anterior
        pygame.mixer.music.load(self.archivo_mp3)
        pygame.mixer.music.play()

        print(f'Reproduciendo: {self.titulo} - {self.artista} ({self.duracion}s)')

    def __str__(self) -> str:
        """Representación de la canción."""
        return f'{self.titulo} - {self.artista} ({self.duracion}s) [{self.genero}] -> {self.archivo_mp3}'


    # MÉTODOS PARA SERIALIZACIÓN

    def to_dict(self) -> dict:
        """
        Convierte la canción a un diccionario serializable a JSON.
        Guardamos solo el nombre del archivo, no la ruta completa.
        """
        return {
            "id": self.id,
            "titulo": self.titulo,
            "artista": self.artista,
            "duracion": self.duracion,
            "genero": self.genero,
            "archivo_mp3": os.path.basename(self.archivo_mp3),
        }


    def from_dict(data: dict, base_path: str) -> "Cancion":
        """
        Crea una Cancion a partir de un diccionario.
        base_path es la carpeta donde están los mp3 en el cliente.
        """
        ruta = os.path.join(base_path, data["archivo_mp3"])
        return Cancion(
            id=data["id"],
            titulo=data["titulo"],
            artista=data["artista"],
            duracion=data["duracion"],
            genero=data["genero"],
            archivo_mp3=ruta,
        )