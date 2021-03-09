import socket

# Crear el socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Puerto
port = 4000

# Estipula la direccion del servidor
direccionServidor = ('localhost', port)

print("conectado...")

# Se conecta al servidor y recibe un mensaje de saludo
s.connect(direccionServidor)
msg = s.recv(1024)
print(msg)

# Le dice al servidor que esta listo para recibir
s.send(b"Listo")

#Crea un archivo para guardar la descarga
filename = "ArchivosRecibidos/re.txt"
file = open (filename, 'wb')

#Guarda la descarga por chunks
while True:
    data = s.recv(512)
    if (len(data) < 1):
        break
    file.write(data)

file.close()
print("Archivo recibido")

# Avisa al servidor de la correcta recepcion
s.send(b"Listo")
