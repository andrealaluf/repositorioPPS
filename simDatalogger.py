#from communicator import communicator
import os
import sys
import threading
import Queue
import random
import communicator as com

os.path.abspath('home/fabio/repositorioPPS')

from Command import Command
from Data import Data


def sendCommand(f):
	while 1:
		entrada = raw_input('>>')
		if entrada[0] == 1:
			comando = Command('Datalogger1','SENSE', 0)
			com.send('client02',comando)
			f.write(comando.getCommand()+' '+comando.getValue()+"  --  "+time.strftime("H:M:S"))
		elif entrada[0] == 2:
			comando = Command('Datalogger1','SETFR', entrada[2:3])
			com.send('client02',comando)
			f.write(comando.getCommand()+' '+comando.getValue()+"  --  "+time.strftime("H:M:S"))	
		elif entrada[0] == 3:
			comando = Command('Datalogger1','STOP', 0)
			com.send('client02',comando)
			f.write(comando.getCommand()+' '+comando.getValue()+"  --  "+time.strftime("H:M:S"))
			f.close()
		else:
			print 'comando erroneo'

def receiveData():
	while 1:
		if com.lenght() > 0:
			dato = com.receive()
			f.write(dato.getValue()+" "+dato.getUnit()+"  --  "+time.strftime("H:M:S"))

try:
	print '--------- Datalogger Simulator -----------'
	print '1 - SENSE'
	print '2 - SETFR <freq>'
	print '3 - STOP'
	
	f = open("datalogger.txt","w")
	com.open()
		
	enviacomando = threading.Thread(target=sendCommand)
	recibedato = threading.Thread(target=receiveData)
	
	enviacomando.start()
	recibedato.start()
	
	while True:
		pass
	
except KeyboardInterrupt:
	f.close()
	com.close()
	