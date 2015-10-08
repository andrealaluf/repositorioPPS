# -*- coding: utf-8 -*-
#!/usr/bin/python
import os
import sys
import threading
import time
import communicator as com
from multiprocessing import Condition

sys.path.insert(0,'/home/pi/win_shared')

from UltrasonicSensorClass import Ultrasonic
from HumidityTemperatureClass import HumidityTemperature
import Data
import Command

# Declara diccionario asumiendo un par de sensores activos
sensorDict = 	{	
					'ULTRASONIC':0,
					'TEMPERATURE':1	
				};

def readCommand(sensorList, conditionList):
	
	# Se leen comandos mientras existan sensores activos
	while len(sensorDict) > 0:
		
		# Pregunta si hay mensajes por recibir
		if com.lenght() > 0: 
			# Recibe el mensaje  en cola
			comando = com.receive()
			
			sensorNumber = sensorDict[comando.getReceiver()]
			#sensorNumber = sensorDict[parsedCommand[0]]
			
			# Adquiere el lock sobre la condicion para garantizar la 
			# exclusion mutua sobre las variables compartidas
			conditionList[sensorNumber].acquire()
			
			# interpreta los comandos  y actua de acuerdo a lo recibido
			if (comando.getCommand() == "SENSE") | (comando.getCommand() == "SETFR"):	
				sensorList[sensorNumber].setSenseFlag(True)
				sensorList[sensorNumber].setFrequency(comando.getValue())
				#sensorList[sensorNumber].setFrequency(int(parsedCommand[2]))				
			else:
				# Si se recibe un STOP sobre un determinado sensor, 
				# se lo elimina del diccionario
				sensorList[sensorNumber].setSenseFlag(False)
				del sensorDict[comando.getReceiver()];
			
			# Despierta los hilos dormidos bajo la condicion y libera el bloqueo
			conditionList[sensorNumber].notify()
			conditionList[sensorNumber].release()
	exit (0)
				
def sendData(sensor, condition, key):
	
	# Cada hilo que atiende a un sensor inicia un bucle mientras el sensor exista. 
	# Cuando el sensor desaparece del diccionario, el hilo termina su ejecucion
	while sensorDict.has_key(key):
		
		# Se adquiere el lock sobre la variable Condition para garantizar 
		# la exclusion mutua sobre la variable frecuencia de cada sensor
		condition.acquire()
		if (sensor.getSenseFlag() == True):
			condition.wait(sensor.getFrequency())		
			
			# Se prepara el dato y se lo envia
			dato = sensor.getData('client03', 5,100,' ')
			#datoAEnviar = str(dato.getData()) + ' ' + dato.getUnit()
			com.send(dato)
			
			# Si el comando recibido es un SENSE, espera por un nuevo comando que 
			# despierte el hilo
			if (sensor.getFrequency() == 0): 
				sensor.setSenseFlag(False)
				condition.wait()			
		condition.release()
	exit (0)

if __name__ == '__main__':

	try:		
		# Inicia modulo comunicador
		com.open()
		sensors = []
		conditions = []
		
		# Inicia las instancias de los sensores y los agrega a una lista
		sensors.append(Ultrasonic(0,[23,24]))
		sensors.append(HumidityTemperature(0,[4]))
		
		# Declara una variable Condition y lanza un hilo por cada sensor
		conditions.append(threading.Condition())
		ultsnd = threading.Thread(target = sendData, args=(sensors[0], conditions[0], 'ULTRASONIC'))		
		
		conditions.append(threading.Condition())
		temp = threading.Thread(target = sendData, args=(sensors[1], conditions[1], 'TEMPERATURE'))	
		
		# Declara hilo para la recepcion de comandos
		receiver = threading.Thread(target = readCommand, args=(sensors, conditions))
	
		# Lanza los hilos
		ultsnd.start()
		temp.start()
		receiver.start()
		
		# El hilo principal queda esperando en un bucle hasta que no haya mas sensores en funcionamiento
		while len(sensorDict) > 0:
			pass
		
		# Se cierra el modulo comunicador
		com.close()
		exit (0)
	
	except KeyboardInterrupt:
		com.close()