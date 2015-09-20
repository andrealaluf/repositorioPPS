#from communicator import communicator
import sys
import threading
import Queue
import random
from Command import Command
from Data import Data

sys.path.append('/home/fabio/Communicator')

import communicator

def inputCommand(queueCommand, f):
	while 1:
		entrada = raw_input('>>')
		if entrada[0] == 1:
			comando = Command('Datalogger1','SENSE', 0)
			queueCommand.put(comando)
			f.write(comando.getCommand()+' '+comando.getValue())
		elif entrada[0] == 2:
			comando = Command('Datalogger1','SETFR', entrada[2:3])
			queueCommand.put(comando)
			f.write(comando.getCommand()+' '+comando.getValue())	
		elif entrada[0] == 3:
			comando = Command('Datalogger1','STOP', 0)
			queueCommand.put(comando)
			f.write(comando.getCommand()+' '+comando.getValue())
			f.close()
		else:
			print 'comando erroneo'

def sendCommand(queueCommand):
	while 1:
		comando = queueCommand.get()
		communicator.send(comando.getSenderID(),comando,True)

def receiveData(queueData):
	while 1:
		queueData.put(communicator.receive())

def inputData(queueData, f):
	while 1:
		dato = queueData.get()
		f.write(dato.getValue()+" "+dato.getUnit())

try:
	print '--------- Datalogger Simulator -----------'
	print '1 - SENSE'
	print '2 - SETFR <freq>'
	print '3 - STOP'
	communicator.open()
	
	queueCommand = Queue(10)
	queueData = Queue(10)
	f = open("datalogger.txt","w")
	comando = threading.Thread(target=inputCommand, args=(queueCommand, f,))
	enviacomando = threading.Thread(target=sendCommand, args=(queueCommand,))
	recibedato = threading.Thread(target=receiveData, args=(queueData,))
	dato = threading.Thread(target=inputData, args=(queueData, f,))
	
except KeyboardInterrupt:
	communicator.close()
