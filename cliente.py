import socket

def start_client():
    # Crear un socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectar el socket al servidor
    server_address = ('localhost', 12345)
    client_socket.connect(server_address)
    nombre = input('Ingrese su nombre: ')

    while True:
        message = input('Mensaje: ')
        client_socket.sendall(nombre.encode('utf-8'))
        client_socket.sendall(message.encode('utf-8'))
        if message == 'QUIT':
            print("Terminaste la conversación")
            client_socket.close()
            break
        else:
            reply = client_socket.recv(1024).decode('utf-8')
            if reply == 'QUIT':
                print("El servidor terminó la conversación")
                client_socket.close()
                break
            else:
                print("Servidor: " + reply)

if __name__ == '__main__':
    start_client()
