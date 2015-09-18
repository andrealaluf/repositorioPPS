import abc
from GPIOSensor import GPIOSensor
from Data import Data
# Sensor de prueba para Linux

class LinuxSensor(GPIOSensor):
	
	def __init__(self,frecuencia, pins):
		GPIOSensor.__init__(self, frecuencia, pins)
		self.tipo = "LINUX"
		
	def setGPIOpins(self):
		pass

	def getData(self):
		return Data(self.tipo, self.sense(), "cm")
		
	def clearSensor(self):
		pass
		
	def getType(self):
		return self.tipo

	def sense(self):
		self.setSense(False)
		return 'LINUX_DATA'

GPIOSensor.register(LinuxSensor)
