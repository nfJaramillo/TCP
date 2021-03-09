import socket
from threading import Thread

# Crear el socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Puerto
port = 4000

# Unir el socket con una direccion ip y un puerto
s.bind(("", port))

# Comienza a escuchar
s.listen(25)

while (True):
    # Acepta la nueva conexion
    c, a = s.accept()
    print("Mensaje de: " + str(a))
    # Envia un mensaje al cliente
    c.send(b"Hola soy el servidor!!")
    c.recv(1024)

    #Selecciona el archivo a enviar
    filename = "ArchivosAEnviar/100.txt"
    file = open(filename, 'rb')
    file_data = file.read()

    #Envia el archivo
    c.send(file_data)
    print("Archivo enviado")

    #Recibe la confirmacion
    c.recv(1024)



    c.close()  # Cierra la conexion