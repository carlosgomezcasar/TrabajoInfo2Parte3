import socket
import threading
import json
import os


# FUNCIONES AUXILIARES PARA ENVÍO Y RECEPCIÓN DE MP3

def recibir_linea(sock):
    """Recibe una línea terminada en '\n'."""
    data = b""
    while not data.endswith(b"\n"):
        chunk = sock.recv(1)
        if not chunk:
            break
        data += chunk
    return data.decode().strip()


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


def recibir_mp3(sock, carpeta_destino):
    header = recibir_linea(sock)
    if not header.startswith("MP3_SIZE:"):
        return None
    size = int(header.split(":")[1])

    header = recibir_linea(sock)
    if not header.startswith("MP3_NAME:"):
        return None
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


# SERVIDOR

USUARIOS_ACTIVOS = {}  # usuario -> True si está conectado
BASE_DATOS = "datos_server"


def manejar_cliente(sock, addr):
    print(f"[+] Conexión aceptada desde {addr}")

    try:
        # 1. LOGIN
        linea = recibir_linea(sock)
        if not linea.startswith("LOGIN:"):
            sock.sendall("ERROR\n".encode())
            sock.close()
            return

        usuario = linea.split(":")[1].strip()

        # Comprobar bloqueo
        if usuario in USUARIOS_ACTIVOS:
            sock.sendall("REJECTED\n".encode())
            sock.close()
            return

        # Bloquear usuario
        USUARIOS_ACTIVOS[usuario] = True
        sock.sendall("OK\n".encode())

        # Carpeta del usuario
        carpeta_usuario = os.path.join(BASE_DATOS, usuario)
        os.makedirs(carpeta_usuario, exist_ok=True)

        # 2. ENVIAR METADATA
        ruta_json = os.path.join(carpeta_usuario, "biblioteca.json")
        if os.path.exists(ruta_json):
            with open(ruta_json, "r", encoding="utf-8") as f:
                data = f.read()
        else:
            data = json.dumps({"canciones": [], "listas": []})

        data_bytes = data.encode()
        sock.sendall(f"METADATA_SIZE:{len(data_bytes)}\n".encode())
        sock.sendall(data_bytes)

        # 3. ENVIAR TODOS LOS MP3 QUE TENGA EL USUARIO
        mp3s = [f for f in os.listdir(carpeta_usuario) if f.lower().endswith(".mp3")]

        sock.sendall(f"NUM_MP3:{len(mp3s)}\n".encode())

        for mp3 in mp3s:
            ruta = os.path.join(carpeta_usuario, mp3)
            enviar_mp3(sock, ruta)


        # 4. RECIBIR NUEVA METADATA DESDE EL CLIENTE
        linea = recibir_linea(sock)
        if linea != "UPLOAD_METADATA":
            raise Exception("Protocolo inválido (se esperaba UPLOAD_METADATA)")

        header = recibir_linea(sock)
        if not header.startswith("SIZE:"):
            raise Exception("Protocolo inválido en metadata")

        tam = int(header.split(":")[1])
        contenido = sock.recv(tam).decode()

        # Guardamos metadata
        with open(ruta_json, "w", encoding="utf-8") as f:
            f.write(contenido)


        # 5. RECIBIR NÚMERO DE MP3
        linea = recibir_linea(sock)
        if not linea.startswith("NUM_MP3:"):
            raise Exception("Protocolo inválido al recibir número de MP3")

        n = int(linea.split(":")[1])

        # Recibir MP3 uno por uno
        for _ in range(n):
            recibir_mp3(sock, carpeta_usuario)


        # 6. LOGOUT
        linea = recibir_linea(sock)
        if linea != "LOGOUT":
            raise Exception("Protocolo inválido en LOGOUT")

        print(f"[+] Usuario {usuario} desconectado limpiamente.")

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        # Liberar usuario
        if usuario in USUARIOS_ACTIVOS:
            USUARIOS_ACTIVOS.pop(usuario)
        sock.close()


def main():
    if not os.path.exists(BASE_DATOS):
        os.makedirs(BASE_DATOS)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)

    print("[Servidor] Esperando conexiones en el puerto 9999...")

    while True:
        sock, addr = server.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(sock, addr), daemon=True)
        hilo.start()


if __name__ == "__main__":
    main()
