import Data
import Command
import threading
import time
from UltrasonicSensorClass import Ultrasonic
from HumidityTemperatureClass import HumidityTemperature

sys.path.append('/home/fabio/Communicator')

import communicator


sensors = 	{	'ULTRASONIC':1,
				'TEMPERATURE':2	
			};

def readCommand(sensors, condition):
	while True:
		condition.acquire()
		if communicator.len() > 0: 
			comando = communicator.receive()
			if comando.getCommand() == "SENSE":
				sensors[dict[comando.getReceiver()]].setSenseFlag(True)
				sensors[dict[comando.getReceiver()]].setFrequency(comando.getValue())
				condition.notify()
				condition.release()
			elif comando.getCommand() == "SETFR":
				sensors[dict[comando.getReceiver()]].setSenseFlag(True)
				sensors[dict[comando.getReceiver()]].setFrequency(comando.getValue())
				condition.notify()	
				condition.release()
			else:
				sensors[dict[comando.getReceiver()]].setSenseFlag(False)
				sensors[dict[comando.getReceiver()]].setFrequency(0)
				condition.wait()	
			condition.release()
				
def sendData(sensor, condition):
	while True:
		condition.acquire()
		if (sensor.getSenseFlag() == True) | (sensor.getFrequency() > 0):
			condition.wait(sensor.getFrequency())
			sensor.setSenseFlag(False)
			communicator.send('Datalogger1', sensor.getData(), True)
		else:
			condition.wait()
		condition.release()

if __name__ == '__main__':

	sensors [0] = Ultrasonic(0,[23,24])
	sensors [1] = HumidityTemperature(0,[4])
	 
	Ucondition = threading.Condition()
	ultsnd = threading.Thread(target="sendData", args=(sensors[0], Ucondition))
	
	Tcondition = threading.Condition()
	temp = threading.Thread(target="sendData", args=(sensors[1], Tcondition))
