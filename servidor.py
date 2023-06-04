import socket
import threading

usuarios = {}

def manejar_cliente(client_socket, client_address):
    usuario = client_socket.recv(1024).decode('utf-8')
    if usuario not in usuarios:
        usuarios[usuario] = {
            'receptor': '',
            'socket': client_socket
        }

    if len(usuarios) > 1:
        respuesta = 'Servidor iniciado y contestando OK'
        for u in usuarios:
            if u != usuario:
                respuesta += f' "{u}" conectado\n '
        respuesta += 'Seleccione un usuario para continuar'
    else:
        respuesta = 'No se ha conectado nadie todavía'
    
    usuarios[usuario]["socket"].sendall(respuesta.encode('utf-8'))

    while True:
        mensaje = client_socket.recv(1024).decode('utf-8')
        if mensaje in usuarios and usuarios[usuario]["receptor"] == '':
            usuarios[usuario]["receptor"] = mensaje
            usuarios[mensaje]["receptor"] = usuario
            respuesta = f"Conexion con {mensaje} correcta :-)"
            usuarios[usuario]["socket"].sendall(respuesta.encode('utf-8'))
        elif usuarios[usuario]["receptor"]:
            if mensaje == 'chao':
                print(f'El usuario {usuario} abandonó la conversación')
                usuarios[usuarios[usuario]["receptor"]]["socket"].sendall(f'{usuario} ha dejado la charla'.encode('utf-8'))
                del usuarios[usuario]
                client_socket.close()
                break
            else:
                res=f'{usuario} ----> {mensaje}'
                usuarios[usuarios[usuario]["receptor"]]["socket"].sendall(res.encode('utf-8'))
        else:
            respuesta = 'Por favor selecciona un receptor,\n'
            for u in usuarios:
                if u != usuario:
                    respuesta += f' "{u}" conectado\n '
            respuesta += 'Seleccione un usuario para continuar'
            usuarios[usuario]["socket"].sendall(respuesta.encode('utf-8'))

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('localhost', 12347)
    server_socket.bind(server_address)

    server_socket.listen(1)
    print("El servidor está escuchando en {}:{}".format(*server_address))

    while True:
        print("Esperando a un cliente...")
        client_socket, client_address = server_socket.accept()
        print("Conexión desde {}:{}".format(*client_address))

        threading.Thread(target=manejar_cliente, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()