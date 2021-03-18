import socket
import threading
import time
import hashlib
import os

# Crear el socket


# Puerto
port = 4000


# Preguntar por el archivo
while True:
    print("Escriba el nombre del archivo a transferir")
    nombreArchivo = input()
    try:
        file = open(nombreArchivo, 'rb')
        file_data = file.read()
        m = hashlib.sha256()
        m.update(file_data)
        hash = m.hexdigest()
        #print("Este es el hash: " + hash)
        break
    except Exception as e :
        print(str(e))

# Preguntar por el numero de conexiones
while True:
    print("Escriba la cantidad de conexiones, minimo 25 ")
    cantConexiones = int(input())
    if(cantConexiones > 0):
        break

conexionesActuales = 0

threadlock = threading.Lock()
def escuchar (puerto):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global port
    global conexionesActuales
    # Unir el socket con una direccion ip y un puerto
    s.bind(("", puerto))
    # Comienza a escuchar
    s.listen(5)
    c, a = s.accept()
    print("Mensaje de: " + str(a))

    with threadlock:
        conexionesActuales += 1

    print("ACtual: " + str(conexionesActuales) + " Esperado: " + str(cantConexiones))
    while conexionesActuales < cantConexiones:

        time.sleep(1)

    print("enviando... " + str(conexionesActuales))
    c.send(hash.encode("utf-8"))
    print(c.recv(13))
    c.send(str(os.path.getsize(nombreArchivo)).encode("utf-8"))
    print(c.recv(12))
    c.sendall(file_data)
    print(c.recv(29))
    c.close()


cantConexiones2 = 0
while cantConexiones2<cantConexiones:
    # Acepta la nueva conexion
    port +=1
    cantConexiones2 +=1
    threading.Thread(target=escuchar, args=(port,)).start()




