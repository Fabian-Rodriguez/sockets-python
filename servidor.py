import socket


def start_server():
    # Crear un socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Asignar dirección IP y puerto al socket
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)

    # Escuchar conexiones entrantes
    server_socket.listen(1)
    print("El servidor está escuchando en {}:{}".format(*server_address))
    usuarios = {}

    while True:
        print("Esperando a un cliente...")
        client_socket, client_address = server_socket.accept()
        print("Conexión desde {}:{}".format(*client_address))
        TEST = True

        while TEST:
            usuario = client_socket.recv(1024).decode('utf-8')
            if usuario not in usuarios:
                usuarios[usuario] = {
                    'receptor': ''
                }
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'Chao':
                print(f'El usuario {usuario} abandonó la conversación')
                client_socket.close()
            elif message in usuarios and usuarios[usuario]["receptor"] == '': 
                usuarios[usuario]["receptor"]=message
                reply = f'''Ya puedes hablar con {message}'''
                client_socket.sendall(reply.encode('utf-8'))
            elif usuarios[usuario]["receptor"] == '':
                nombres=''
                for u in usuarios:
                    nombres+=f'{u},'
                reply = f'''Actualmente hay {len(usuarios)} {'usuarios' if len(usuarios)>0 else 'usuario'} los cuales son: {nombres} escriba el nombre para continuar'''
                client_socket.sendall(reply.encode('utf-8'))
            elif message not in usuarios: 
                reply = f'''Ingrese un usuario valido, por favor'''
                client_socket.sendall(reply.encode('utf-8'))
            else:
                print(f'''Usuario: {usuario} con mensaje: {message}''')
                reply = 'Por favor agregue un usuario a la conversacion'
                client_socket.sendall(reply.encode('utf-8'))
                if reply == 'QUIT':
                    print("Terminaste la conversación")
                    client_socket.close()
                    break


if __name__ == '__main__':
    start_server()
