import socket
import json
import os
from musica.plataforma import PlataformaMusical
from musica.cancion import Cancion
from musica.lista_reproduccion import ListaReproduccion
from app import menu_canciones, menu_listas, menu_reproduccion


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


    # MENÚS
    while True:
        print("\n=== Plataforma Musical (cliente) ===")
        print("1) Gestionar canciones")
        print("2) Gestionar listas")
        print("3) Reproducción")
        print("0) Salir")
        opc = input("> ")

        if opc == "1":
            menu_canciones(plataforma)
        elif opc == "2":
            menu_listas(plataforma)
        elif opc == "3":
            menu_reproduccion(plataforma)
        elif opc == "0":
            break


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