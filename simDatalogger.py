#from communicator import communicator
import sys
import threading
import Queue
import random
from Command import Command
from Data import Data

sys.path.append('/home/fabio/Communicator')

import communicator

def sendCommand(f):
	while 1:
		entrada = raw_input('>>')
		if entrada[0] == 1:
			comando = Command('Datalogger1','SENSE', 0)
			communicator.send(comando.getSenderID(),comando,True)
			f.write(comando.getCommand()+' '+comando.getValue()+"  --  "+time.strftime("H:M:S"))
		elif entrada[0] == 2:
			comando = Command('Datalogger1','SETFR', entrada[2:3])
			communicator.send(comando.getSenderID(),comando,True)
			f.write(comando.getCommand()+' '+comando.getValue()+"  --  "+time.strftime("H:M:S"))	
		elif entrada[0] == 3:
			comando = Command('Datalogger1','STOP', 0)
			communicator.send(comando.getSenderID(),comando,True)
			f.write(comando.getCommand()+' '+comando.getValue()+"  --  "+time.strftime("H:M:S"))
			f.close()
		else:
			print 'comando erroneo'

def receiveData(queueData):
	while 1:
		if communicator.len() != 0:
			dato = communicator.receive()
			f.write(dato.getValue()+" "+dato.getUnit()+"  --  "+time.strftime("H:M:S"))

try:
	print '--------- Datalogger Simulator -----------'
	print '1 - SENSE'
	print '2 - SETFR <freq>'
	print '3 - STOP'
	
	f = open("datalogger.txt","w")
	communicator.open()
		
	enviacomando = threading.Thread(target=sendCommand, args=(queueCommand,))
	recibedato = threading.Thread(target=receiveData, args=(queueData,))
	
except KeyboardInterrupt:
	f.close()
	communicator.close()
	