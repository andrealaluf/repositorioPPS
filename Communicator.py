import socket  
import time

class Communicator(object):

	def __init__(self):
		self.server = socket.socket() 
		self.client = socket.socket()

	def open(self, clientport, serverport):  
		self.server.bind(("localhost", clientport))  
		self.server.listen(1)  
  		self.sc, addr = self.server.accept()
  		time.sleep(10)
  		self.client.connect("localhost", serverport)
  
  	def receive(self):
  		return self.sc.recv(1024)  
		#sc.send(recibido)

	def send(self, mensaje):
		self.client.send(mensaje)  


	def close(self):
		self.sc.close()  
		self.server.close() 
		self.client.close()