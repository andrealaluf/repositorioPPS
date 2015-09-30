import threading
import time
import communicator as com
from multiprocessing import Condition

os.path.insert(0,'/home/pi/win_shared')

from UltrasonicSensorClass import Ultrasonic
from HumidityTemperatureClass import HumidityTemperature
import Data
import Command

sensorDict = 	{	'ULTRASONIC':1,
					'TEMPERATURE':2	
				};

def readCommand(sensorList, conditionList, flag):
	while True:
		if com.lenght() > 0: 
			comando = com.recieve()
			sensorNumber = sensorDict[comando.getReceiver()]
			if comando.getCommand() == "SENSE":
				coditionList[sensorNumber].acquire()
				sensorList[sensorNumber].setSenseFlag(True)
				sensorList[sensorNumber].setFrequency(comando.getValue())
				flag = True				
				coditionList[sensorNumber].notify()
				coditionList[sensorNumber].release()

			elif comando.getCommand() == "SETFR":
				coditionList[sensorNumber].acquire()
				sensorList[sensorNumber].setSenseFlag(False)
				sensorList[sensorNumber].setFrequency(comando.getValue())
				flag = True
				coditionList[sensorNumber].notify()
				coditionList[sensorNumber].release()		
			else:
				coditionList[sensorNumber].acquire()
				sensorList[sensorNumber].setSenseFlag(False)
				sensorList[sensorNumber].setFrequency(comando.getValue())
				flag = False
				coditionList[sensorNumber].wait()	
				
def sendData(sensor, condition):
	while True:
		condition.acquire()
		if (sensor.getSenseFlag() == True) | (sensor.getFrequency() > 0):
			condition.wait(sensor.getFrequency())
			sensor.setSenseFlag(False)
			dato = sensor.getData()
			print dato.getValue(),' ',dato.getUnit()
			com.send('client03', dato)       
		else:
			condition.wait()
		condition.release()


if __name__ == '__main__':

	try:
		com.open()
		
		flag = True
		sensors [0] = Ultrasonic(0,[23,24])
		sensors [1] = HumidityTemperature(0,[4])		 
		conditions[0] = threading.Condition()
		ultsnd = threading.Thread(target = sendData, args=(sensors[0], conditions[0]))		
		conditions[1] = threading.Condition()
		temp = threading.Thread(target = sendData, args=(sensors[1], conditions[1]))	
		receiver = threading.Thread(target = receiveCommand, args=(sensors, conditions, flag))
	
		ultsnd.start()
		temp.start()
		receiver.start()
		
		while flag:
			pass
		com.close()
	
	except KeyboardInterrupt:
		com.close()