import socket  

class Client(object):

	def __init__(self):
		self.s = socket.socket()   

	def open(self, port):
		self.s.connect(("localhost", port))  

	def send(self, mensaje):
		self.s.send(mensaje)  

	def close(self):
		self.s.close()

# cliente = Client()
# try:
# 	cliente.open()
# 	while True:  
# 		mensaje = raw_input(">>")
# 		cliente.send(mensaje)
# except KeyboardInterrupt:
# 	cliente.close()
