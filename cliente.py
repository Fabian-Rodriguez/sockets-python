import socket
import threading

def manejar_mensajes_recibidos(client_socket):
    while True:
        mensaje = client_socket.recv(1024).decode('utf-8')
        print("\nMensaje del servidor: ", mensaje)

def start_client():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    direccion_ip = input("Introduce la direccion ip: ")
    puerto = input("Introduce el puerto: ")

    server_address = (f'{direccion_ip}', int(puerto))
    client_socket.connect(server_address)

    nombre = input("Introduce tu nombre: ")
    client_socket.sendall(nombre.encode('utf-8'))

    threading.Thread(target=manejar_mensajes_recibidos, args=(client_socket,)).start()

    while True:
        mensaje = input(f"{nombre}> ")
        client_socket.sendall(mensaje.encode('utf-8'))
        if mensaje == 'chao':
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()

