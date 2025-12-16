import socket
import json
import os
import copy  # Para copiar estados de la plataforma sin compartir referencias
from musica.plataforma import PlataformaMusical
from musica.cancion import Cancion
from musica.lista_reproduccion import ListaReproduccion
from app import menu_canciones, menu_listas, menu_reproduccion
from lista_historial import HistorialEstados


# FUNCIONES AUXILIARES PARA ENVÍO Y RECEPCIÓN DE MP3

def recibir_linea(sock):
    data = b""
    while not data.endswith(b"\n"):
        chunk = sock.recv(1)
        if not chunk:
            break
        data += chunk
    return data.decode().strip()


def recibir_mp3(sock, carpeta_destino):
    header = recibir_linea(sock)
    size = int(header.split(":")[1])

    header = recibir_linea(sock)
    nombre = header.split(":")[1]

    ruta = os.path.join(carpeta_destino, nombre)

    with open(ruta, "wb") as f:
        restantes = size
        while restantes > 0:
            chunk = sock.recv(min(1024, restantes))
            if not chunk:
                break
            f.write(chunk)
            restantes -= len(chunk)

    return ruta


def enviar_mp3(sock, ruta):
    size = os.path.getsize(ruta)
    nombre = os.path.basename(ruta)

    sock.sendall(f"MP3_SIZE:{size}\n".encode())
    sock.sendall(f"MP3_NAME:{nombre}\n".encode())

    with open(ruta, "rb") as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            sock.sendall(chunk)


# CLIENTE

def main():
    usuario = input("Introduce tu usuario: ").strip()
    host = input("IP del servidor (enter = localhost): ").strip() or "localhost"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 9999))

    # 1. LOGIN
    sock.sendall(f"LOGIN:{usuario}\n".encode())

    resp = recibir_linea(sock)
    if resp == "REJECTED":
        print("Ese usuario ya está siendo usado. Intenta más tarde.")
        sock.close()
        return

    print("[Cliente] Conectado correctamente.")

    # Carpeta local
    carpeta_local = f"datos_cliente_{usuario}"
    os.makedirs(carpeta_local, exist_ok=True)

    # 2. RECIBIR METADATA
    linea = recibir_linea(sock)
    size = int(linea.split(":")[1])
    metadata = sock.recv(size).decode()

    data = json.loads(metadata)
    plataforma = PlataformaMusical.from_dict(data, carpeta_local)

    # 3. RECIBIR MP3
    linea = recibir_linea(sock)
    num_mp3 = int(linea.split(":")[1])

    for _ in range(num_mp3):
        recibir_mp3(sock, carpeta_local)

    # === HISTORIAL DE ESTADOS (DESHACER / REHACER) ===
    historial = HistorialEstados()
    # Estado inicial: tras sincronizar con el servidor
    historial.inicializar_con_estado(copy.deepcopy(plataforma))

    # MENÚS
    while True:
        print("\n=== Plataforma Musical ===")
        print("1) Gestionar canciones")
        print("2) Gestionar listas")
        print("3) Reproducción")

        # Mostrar opciones de deshacer/rehacer según disponibilidad
        if historial.puede_deshacer():
            print("4) Deshacer última acción")
        else:
            print("4) Deshacer última acción (no disponible)")

        if historial.puede_rehacer():
            print("5) Rehacer última acción deshecha")
        else:
            print("5) Rehacer última acción deshecha (no disponible)")

        print("0) Salir")
        opc = input("> ").strip()

        if opc == "1":
            # Guardamos el estado anterior como texto para detectar cambios
            estado_antes = json.dumps(plataforma.to_dict(), sort_keys=True)

            menu_canciones(plataforma)

            estado_despues = json.dumps(plataforma.to_dict(), sort_keys=True)
            # Si ha cambiado algo, registramos nuevo estado en el historial
            if estado_despues != estado_antes:
                historial.registrar_nuevo_estado(copy.deepcopy(plataforma))

        elif opc == "2":
            estado_antes = json.dumps(plataforma.to_dict(), sort_keys=True)

            menu_listas(plataforma)

            estado_despues = json.dumps(plataforma.to_dict(), sort_keys=True)
            if estado_despues != estado_antes:
                historial.registrar_nuevo_estado(copy.deepcopy(plataforma))

        elif opc == "3":
            menu_reproduccion(plataforma)

        elif opc == "4":
            # DESHACER
            if historial.puede_deshacer():
                plataforma = historial.deshacer()
                print("[Historial] Se ha deshecho la última acción.")
            else:
                print("[Historial] No hay acciones que se puedan deshacer.")

        elif opc == "5":
            # REHACER
            if historial.puede_rehacer():
                plataforma = historial.rehacer()
                print("[Historial] Se ha rehecho la última acción.")
            else:
                print("[Historial] No hay acciones que se puedan rehacer.")

        elif opc == "0":
            break

        else:
            print("Opción no válida. Intenta de nuevo.")

    # 4. ENVIAR METADATA
    metadata = json.dumps(plataforma.to_dict())
    metadata_bytes = metadata.encode()

    sock.sendall("UPLOAD_METADATA\n".encode())
    sock.sendall(f"SIZE:{len(metadata_bytes)}\n".encode())
    sock.sendall(metadata_bytes)

    # 5. ENVIAR MP3
    mp3s = [f for f in os.listdir(carpeta_local) if f.lower().endswith(".mp3")]

    sock.sendall(f"NUM_MP3:{len(mp3s)}\n".encode())
    for mp3 in mp3s:
        enviar_mp3(sock, os.path.join(carpeta_local, mp3))

    # 6. LOGOUT
    sock.sendall("LOGOUT\n".encode())
    sock.close()

    print("Datos sincronizados correctamente. Adiós.")


if __name__ == "__main__":
    main()
