import socket
import threading
import hashlib



# Puerto inicial, cada thread cliente estara en un puerto diferente
# Desde el 4001 hasta la cantidad de conexiones esperadas sumando de 1 en 1
port = 4000

# Pide la direccion del servidor por consola
print("Escriba la direccion ip del servirdor (Ej. 127.0.0.1)")
ip = input()

# Pide la cantidad de clientes por consola
print("Escriba la cantidad de clientes (Ej. 25)")
cantClientes = int(input())

# Crea una variable que contara la cantidad de clientes creados
clientesActuales = 0

# Funcion que ejecutaran los threads, donde ocurre la conexion, la recepcion y la confirmacion
def recibir (num):
    # Crea el socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    direccionServidor = (ip, port+num)
    # Se conecta al servidor
    s.connect(direccionServidor)

    # Recibe el hash esperado del archivo
    hash = s.recv(1024).decode("utf-8")
    s.send(b"Hash Recibido")

    # Recibe el tamano esperado del archivo
    tamEsperado = int(s.recv(1024).decode("utf-8"))
    s.send(b"Tam Recibido")

    # Recibe la extension del archivo
    extension = s.recv(3).decode("utf-8")
    s.send(b"Ext Recibida")

    # Crea un archivo para guardar la descarga
    filename = "ArchivosRecibidos/Cliente"+str(num)+"-Prueba-"+str(cantClientes)+"."+extension
    file = open(filename, 'wb')

    # Variable que cuenta el tamano del archivo que se va recibiendo
    tam = 0
    # Contador para los paquetes que se recibieron
    contador = 0
    # Guarda la descarga por chunks de 512B hasta que el tamano en Bytes recibido sea igual al esperado
    while True:
        contador += 1
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
    # Calcula el hash del archivo recibido
    hash2 = m.hexdigest()

    # Confirma que sean inguales los hash y envia la confirmacion de si es correcto o no
    if(hash == hash2):
        print("El hash es igual" + " - " +"Hash recibido: " + str(hash) + " - " + "Hash calculado: " + str(hash2) )
        s.send(("Archivo Recibido y verificado").encode("utf-8"))

    else:
        print("El hash esta mal" + " - " + "Hash recibido: " + str(hash) + " - " + "Hash calculado: " + str(hash2))
        s.send(("Archivo Recibido y con fallo ").encode("utf-8"))

    # Envia la cantidad de paquetes recibidos
    s.send(str(contador).encode("utf-8"))

    # Cierra la conexion con el servidor
    s.close()

# Loop que crea y ejecuta tantos cleintes como fueron indicados por consola
# Les pasa por parametro un id de cliente
print("Esperando para recibir...")
while clientesActuales<cantClientes:
    clientesActuales +=1
    threading.Thread(target=recibir, args=(clientesActuales,)).start()


