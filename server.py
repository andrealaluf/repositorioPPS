import socket  
  
class Server(object):

	def __init__(self):
		self.server = socket.socket() 

	def open(self, port):  
		self.server.bind(("localhost", port))  
		self.server.listen(1)  
  		self.sc, addr = self.server.accept()  
  
  	def receive(self):
  		return self.sc.recv(1024)  
		#sc.send(recibido)

	def close(self):
		self.sc.close()  
		self.server.close() 


# comm = Server()
# try:
# 	comm.open()
# 	while True:
# 		print comm.receive()
# except KeyboardInterrupt:
# 	comm.close()