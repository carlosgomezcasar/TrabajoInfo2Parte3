from musica.plataforma import PlataformaMusical
from musica.cancion import Cancion
from musica.lista_reproduccion import ListaReproduccion


def pedir_int(msg: str) -> int:
    """Lee un número entero desde consola con validación."""
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Por favor, introduce un número válido.")


def menu_canciones(plataforma):
    """Menú para gestionar canciones en la plataforma."""
    while True:
        print('\n--- Gestión de canciones ---')
        print('1) Añadir canción')
        print('2) Modificar canción')
        print('3) Eliminar canción')
        print('4) Listar canciones')
        print('0) Volver')
        opc = pedir_int('> ')

        if opc == 1:
            # Añadir canción
            print('\n--- Añadir canción ---')
            titulo = input('Título: ')
            artista = input('Artista: ')
            duracion = pedir_int('Duración (segundos): ')
            genero = input('Género: ')
            archivo = input('Ruta a archivo MP3: ')

            if plataforma.registrar_cancion(titulo, artista, duracion, genero, archivo):
                print('Canción añadida correctamente')
            else:
                print('No se pudo añadir la canción. La canción ya existe')

        elif opc == 2:
            # Modificar canción
            print('\n--- Modificar canción ---')
            if not plataforma.canciones:
                print('No hay canciones registradas')
                continue

            print('\nCanciones disponibles:')
            for c in plataforma.canciones:
                print(f'{c.id}) {c.titulo} - {c.artista} ({c.duracion}s)')
            
            id_cancion = pedir_int('Selecciona número de la canción (0 para cancelar): ')
            if id_cancion == 0:
                break

            # Buscar la canción seleccionada
            cancion = next((c for c in plataforma.canciones if c.id == id_cancion), None)
            if not cancion:
                print('No se encontró una canción con ese ID.')
                continue

            # Pedir nuevos valores (mantener si se pulsa Enter)
            nuevo_titulo = input('Nuevo título (enter para dejar): ') or cancion.titulo
            nuevo_artista = input('Nuevo artista (enter para dejar): ') or cancion.artista

            nueva_duracion_txt = input('Nueva duración (enter para dejar): ')
            if nueva_duracion_txt.strip() == "":
                nueva_duracion = cancion.duracion
            else:
                nueva_duracion = int(nueva_duracion_txt)

            nuevo_genero = input('Nuevo género (enter para dejar): ') or cancion.genero
            nuevo_archivo = input('Nueva ruta MP3 (enter para dejar): ') or cancion.archivo_mp3

            if plataforma.editar_cancion(id_cancion, nuevo_titulo, nuevo_artista, nueva_duracion, nuevo_genero, nuevo_archivo):
                print('Modificada')
            else:
                print('No se encontró una canción con ese ID.')


        elif opc == 3:
            # Eliminar canción
            print('\n--- Eliminar canción ---')
            if not plataforma.canciones:
                print('No hay canciones registradas.')
                continue
            
            print('Canciones disponibles:')
            for c in plataforma.canciones:
                print(f'{c.id}) {c.titulo} - {c.artista} ({c.duracion}s)')
            
            id_cancion = pedir_int('Selecciona número de la canción (0 para cancelar): ')
            if id_cancion == 0:
                break
            
            # Buscar la canción seleccionada
            cancion = next((c for c in plataforma.canciones if c.id == id_cancion), None)
            if not cancion:
                print('No se encontró una canción con ese ID.')
                continue

            if plataforma.eliminar_cancion(id_cancion):
                print('Eliminada')
            else:
                print('No se encontró una canción con ese ID.')

        elif opc == 4:
            # Listar canciones
            if not plataforma.canciones:
                print('No hay canciones registradas.')
            else:
                print('\n--- Listar canciones ---')
                for c in plataforma.canciones:
                    print(f'{c.id}) {c}')

        elif opc == 0:
            break

        else:
            print('Opción inválida. Inténtalo de nuevo.')


def menu_listas(plataforma):
    """Menú para gestionar listas de reproducción."""
    while True:
        print('\n--- Gestión de listas ---')
        print('1) Crear lista')
        print('2) Eliminar lista')
        print('3) Ver contenido de lista')
        print('4) Añadir canciones a lista')
        print('5) Eliminar canción de lista')
        print('0) Volver')
        opc = pedir_int('> ')

        if opc == 1:
            # Crear lista
            print('\n--- Crear lista ---')
            nombre = input('Nombre de la lista: ')
            if plataforma.crear_lista(nombre):
                print('Creada')
            else:
                print('Ya existe una lista con ese nombre.')

        elif opc == 2:
            # Eliminar lista
            print('\n--- Eliminar lista ---')
            if not plataforma.listas:
                print('No hay listas creadas.')
                continue

            print('Listas disponibles:')
            for i, lista in enumerate(plataforma.listas, start=1):
                print(f'{i}) {lista.nombre}')

            indice = pedir_int('Selecciona número de la lista (0 para cancelar): ')
            if indice == 0:
                continue
            if indice < 1 or indice > len(plataforma.listas):
                print('Número de lista no válido.')
                continue

            lista = plataforma.listas[indice - 1]
            if plataforma.borrar_lista(lista.nombre):
                print(f'Lista "{lista.nombre}" eliminada.')
            else:
                print('No se encontró ninguna lista con ese nombre.')

        elif opc == 3:
            # Ver contenido de una lista
            print('\n--- Ver contenido de una lista ---')
            if not plataforma.listas:
                print('No hay listas creadas.')
                continue

            print('Listas disponibles:')
            for i, lista in enumerate(plataforma.listas, start=1):
                print(f'{i}) {lista.nombre}')

            indice = pedir_int('Selecciona número de la lista (0 para cancelar): ')
            if indice == 0:
                continue
            if indice < 1 or indice > len(plataforma.listas):
                print('Número de lista no válido.')
                continue

            lista = plataforma.listas[indice - 1]

            if not lista.canciones:
                print('La lista está vacía.')
            else:
                for id_c in lista.canciones:
                    cancion = next((c for c in plataforma.canciones if c.id == id_c), None)
                    if cancion:
                        print(f'{id_c}) {cancion}')

        elif opc == 4:
            # Añadir canciones a lista
            print('\n--- Añadir canciones a una lista ---')
            if not plataforma.listas:
                print('No hay listas disponibles.')
                continue
            if not plataforma.canciones:
                print('No hay canciones registradas.')
                continue

            print('Listas disponibles:')
            for i, lista in enumerate(plataforma.listas, start=1):
                print(f'{i}) {lista.nombre}')

            indice_lista = pedir_int('Selecciona número de la lista (0 para cancelar): ')
            if indice_lista == 0:
                continue
            if indice_lista < 1 or indice_lista > len(plataforma.listas):
                print('Número de lista no válido.')
                continue

            lista = plataforma.listas[indice_lista - 1]

            print('Canciones disponibles para añadir:')
            for c in plataforma.canciones:
                print(f'{c.id}) {c}')

            id_cancion = pedir_int('Selecciona número de la canción a añadir (0 para cancelar): ')
            if id_cancion == 0:
                continue

            if lista.anadir_cancion(id_cancion):
                print('Añadida')
            else:
                print('La canción ya está en la lista o el ID no es válido.')

        elif opc == 5:
            # Eliminar canción de lista
            print('\n--- Eliminar canción de una lista ---')
            if not plataforma.listas:
                print('No hay listas creadas.')
                continue

            print('Listas disponibles:')
            for i, lista in enumerate(plataforma.listas, start=1):
                print(f'{i}) {lista.nombre}')

            indice = pedir_int('Selecciona número de la lista (0 para cancelar): ')
            if indice == 0:
                continue
            if indice < 1 or indice > len(plataforma.listas):
                print('Número de lista no válido.')
                continue

            lista = plataforma.listas[indice - 1]

            if not lista.canciones:
                print('La lista está vacía.')
                continue

            print('\n--- Canciones en la lista ---')
            for id_c in lista.canciones:
                cancion = next((c for c in plataforma.canciones if c.id == id_c), None)
                if cancion:
                    print(f'{id_c}) {cancion}')

            id_cancion = pedir_int('Selecciona número de la canción a eliminar (0 para cancelar): ')
            if id_cancion == 0:
                continue

            if lista.quitar_cancion(id_cancion):
                print('Eliminada')
            else:
                print('Esa canción no estaba en la lista.')

        elif opc == 0:
            break

        else:
            print('Opción inválida. Inténtalo de nuevo.')



def menu_reproduccion(plataforma):
    """Menú para la reproducción de canciones."""
    while True:
        print('\n--- Reproducción ---')
        if not plataforma.listas:
            print('No hay listas disponibles para reproducir.')
            return

        print('Listas disponibles:')
        for i, lista in enumerate(plataforma.listas, start=1):
            num_canciones = len(lista.canciones)
            print(f'{i}) {lista.nombre} ({num_canciones} canciones)')
        print('0) Volver')

        indice = pedir_int('Selecciona lista: ')
        if indice == 0:
            break
        if indice < 1 or indice > len(plataforma.listas):
            print('Número de lista no válido.')
            continue

        lista = plataforma.listas[indice - 1]

        if not lista.canciones:
            print('La lista está vacía.')
            continue

        indice_cancion = 0

        while True:
            # Obtener canción actual
            id_cancion = lista.canciones[indice_cancion]
            cancion = next((c for c in plataforma.canciones if c.id == id_cancion), None)

            if not cancion:
                print('Error: una de las canciones de la lista no existe.')
                break

            # Mostrar información y reproducir
            cancion.reproducir()

            # Estas son las opciones de navegación
            print('n) Siguiente, p) Anterior, s) Salir reproducción')
            opcion = input('> ').strip().lower()

            if opcion == 'n':
                indice_cancion += 1
                if indice_cancion >= len(lista.canciones):
                    indice_cancion = 0  # Vuelve al inicio
            elif opcion == 'p':
                indice_cancion -= 1
                if indice_cancion < 0:
                    indice_cancion = len(lista.canciones) - 1  # Vuelve al final
            elif opcion == 's':
                break
            else:
                print('Opción no válida.')



def main():
    plataforma = PlataformaMusical()
    while True:
        print('\n=== Plataforma Musical ===')
        print('1) Gestionar canciones')
        print('2) Gestionar listas')
        print('3) Reproducción')
        print('0) Salir')
        opc = pedir_int('> ')
        if opc == 1:
            menu_canciones(plataforma)
        elif opc == 2:
            menu_listas(plataforma)
        elif opc == 3:
            menu_reproduccion(plataforma)
        elif opc == 0:
            print('Hasta luego')
            break
        else:
            print('Opción inválida')


if __name__ == '__main__':
    main()
