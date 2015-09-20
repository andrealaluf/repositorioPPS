import time
import threading
from Data import Data
from Command import Command
from LinuxSensor import LinuxSensor
import random
from server import Server
from client import Client
import comunicador as com

def sendData():
	while flag:
		condition.acquire()
		frequency = sensor.getFrequency()
		if (sensor.getSense() == False) & (frequency == 0):
			condition.wait()
		else:
			condition.wait(frequency)
			com.send(client, sensor.getData())
		condition.release()

def receiveCommand ():
	while flag:
		comando = com.receive(server)
		condition.acquire()
		if comando[0:4] == 'SENSE':
			sensor.setSense(True)
		else:
			sensor.setSense(False)

		sensor.setFrequency(comando[6:7])
		if (sensor.getFrequency() > 0) | (sensor.getSense() == True):
			condition.notify()
		condition.release()
		

if __name__=="__main__":
	
	sensor = LinuxSensor(0,[3])
	condition = threading.Condition()		
	frequency = 0

	server = Server()
	client = Client()
	com.opener(server,client,9999,9998)
	flag = True
	thserver = threading.Thread(target=receiveCommand)
	thclient = threading.Thread(target=sendData)
	server.start()
	client.start()


	while flag: 
		pass
	
	com.close(server,client)
