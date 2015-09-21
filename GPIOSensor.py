import abc
from Sensor import Sensor
import RPi.GPIO as GPIO

class GPIOSensor(Sensor):
	__metaclass__ = abc.ABCMeta

	def __init__(self, frecuencia, pins):
		Sensor.__init__(self, frecuencia)
		self.pins = pins		# ubicacion es un arreglo que contiene el numero de los pines en modo BCM

	
	def clearSensor(self):
		GPIO.cleanup()
	
	def getGPIOpins(self):
		return self.ubicacion

	@abc.abstractmethod
	def setGPIOpins(self):
		""" Establece los pines del sensor """
		pass

Sensor.register(GPIOSensor)