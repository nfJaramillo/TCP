import socket
import threading
import hashlib



# Puerto
port = 4000

# Estipula la direccion del servidor
print("Escriba la direccion ip del servirdor")
ip = input()




# Estipula la cantidad de clientes
while True:
    print("Escriba la cantidad de clientes, minimo 25")
    cantClientes = int(input())
    if (cantClientes > 0):
        break

clientesActuales = 0




def recibir (num):
    # Crear el socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    direccionServidor = (ip, port+num)
    s.connect(direccionServidor)

    hash = s.recv(1024).decode("utf-8")
    s.send(b"Hash Recibido")
    print("Hash Recibido")

    tamEsperado = int(s.recv(1024).decode("utf-8"))
    s.send(b"Tam Recibido")
    print("tam: " + str(tamEsperado))

    # Crea un archivo para guardar la descarga
    filename = "ArchivosRecibidos/re"+str(num)+".txt"
    file = open(filename, 'wb')

    # Guarda la descarga por chunks
    tam = 0
    while True:
        data = s.recv(512)
        tam += len(data)
        if (tam == tamEsperado):
            file.write(data)
            break
        file.write(data)
    file.close()
    print("Archivo recibido")
    # Reabrir archivo para el hash
    file = open(filename, 'rb')
    file_data = file.read()
    m = hashlib.sha256()
    m.update(file_data)
    hash2 = m.hexdigest()
    if(hash == hash2):
        print("El hash es igual" + " - " +"Hash recibido: " + str(hash) + " - " + "Hash calculado: " + str(hash2) )
        s.send(b"Archivo Recibido y verificado")
    else:
        print("El hash esta mal" + " - " + "Hash recibido: " + str(hash) + " - " + "Hash calculado: " + str(hash2))


# Crea todos lo clientes

while clientesActuales<cantClientes:
    clientesActuales +=1
    threading.Thread(target=recibir, args=(clientesActuales,)).start()


