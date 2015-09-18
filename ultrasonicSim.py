import os
import sys
import time
import threading
####-------------- importar communicator
sys.path.append('/home/pi/Communicator')
from communicator import communicator
from Queue import Queue
from Data import Data
from Command import Command
from UltrasonicSensorClass import Ultrasonic


def readSensor():
	while 1:
		condition.acquire()
		frequency = sensor.getFrequency()
		if ((sensor.getSense() == False) & (frequency == 0)):
			condition.wait()
		else:
			condition.wait(frequency)
			communicator.send('Datalogger1',sensor.getData(),True)
		condition.release()
		
def receiveCommand ():
	while 1:
		comando = communicator.receive()
		condition.acquire()
		if comando.getCommand() == 'SENSE':
			sensor.setSense(True)
			condition.notify()
		elif comando.getCommand() == 'SETFR':
			sensor.setSense(False)
			sensor.setFrequency(comando.getValue())
			condition.notify()
		elif:
			sensor.setSense(False)
			sensor.setFrequency(0)
		condition.release()
		
try:
	if __name__=="__main__":
		pines = [23,24]	
		sensor = Ultrasonic(0, pines)

		condition = threading.Condition()		

		dataThread = threading.Thread(target=readSensor) 
		commandThread = threading.Thread(target=receiveCommand)

		dataThread.start()
		commandThread.start()

		while 1: pass
except KeyboardInterrupt:
    sensor.clearSensor()