import os
import sys
import threading
import random
import time
import communicator as com
import contactList

sys.path.insert(0, '/home/fabio/repositorioPPS')

from Command import Command
from Data import Data

sensorReceiver = {}
command = 	{
				'1':"SENSE",
				'2':"SETFR",
				'3':"STOP"
			};

def sendCommand(f):
	print '--------- Datalogger Simulator -----------'
	while len(sensorReceiver) > 0:
		print 'Ingrese uno de los siguientes comandos:'
		
		for key,val in sorted(command.items()):
			print " "*5,key, ":", val
		
		commandInput = raw_input('>>')
		if command.has_key(commandInput):	
			print 'Ingrese un sensor destinatario'
			for key,val in sorted(sensorReceiver.items()):
				print " "*5,key, ":", val
			sensorInput = raw_input('>>')
			
			if sensorReceiver.has_key(sensorInput):
				if commandInput == '1':
					frequency = 0
				elif commandInput == '2':
					print 'Ingrese una valor de frecuencia'
					frequency = raw_input('>>')
				else:
					frequency = 0
					
				comando = Command(sensorReceiver[sensorInput],'client03' , 5, 100, ' ',command[commandInput], frequency)
				com.send(comando)
				f.write(comando.getReceiver().center(15)+ comando.getCommand().center(10) +str(comando.getValue()).center(10)
					+'-'.center(10)+'-'.center(10)+ time.strftime("%H:%M:%S").center(10)+'\n')
				if commandInput == '3':
					del sensorReceiver[sensorInput];
			else: 
				print 'el sensor no existe\n'
		else:
			print 'comando erroneo\n'
	exit(0)

# Metodo que ejecutara el hilo encargado de recibir los datos y escribirlos en un archivo
def receiveData(f):
	while len(sensorReceiver) > 0:
		if com.lenght() > 0:
			dato = com.receive()
			print dato.getSender()
			f.write(dato.getSender().center(15)+'-'.center(10)+'-'.center(10)+str(dato.getData()).center(10)+dato.getUnit().center(10)+time.strftime("%H:%M:%S").center(10)+'\n')
	exit(0)

try:
	f = open("salida.txt","w")
	f.write('SENSOR'.center(15)+'COMANDO'.center(10)+'VALOR'.center(10)+'DATO'.center(10)+'UNIDAD'.center(10)+'TIEMPO'.center(10)+'\n\n')
	com.open()

	# Se arma diccionario con los sensores registrados
	for i in range(len(contactList.allowedIpAddress)):
		sensorReceiver.setdefault(str(i+1))
		sensorReceiver[str(i+1)]=contactList.allowedIpAddress.keys()[i]
	
	# Se crean hilos para la ejecucion del componente externo
	enviacomando = threading.Thread(target=sendCommand, args=(f,))
	recibedato = threading.Thread(target=receiveData, args=(f,))
	
	# Se lanzan los hilos
	enviacomando.start()
	recibedato.start()
	
	while len(sensorReceiver) > 0:
		pass
	
	f.close()
	com.close()
	exit(0)
	
except KeyboardInterrupt:
	f.close()
	com.close()
	