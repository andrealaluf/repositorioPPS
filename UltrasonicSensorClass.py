import time
import abc
import RPi.GPIO as GPIO
from Data import Data
from GPIOSensor import GPIOSensor

class Ultrasonic(GPIOSensor):
	
	def __init__(self, frecuencia, pins):
		GPIOSensor.__init__(self, frecuencia, pins)
		self.tipo = "ULTRASONIC"
		GPIO.setmode(GPIO.BCM) # Usa el sistema de nombramiento BCM - la otra alternativa es BOARD
		self.setGPIOpins()

	def setGPIOpins(self):
		self.TRIG = self.pins[0]
		self.ECHO = self.pins[1]
		GPIO.setup(self.TRIG,GPIO.OUT) 
		GPIO.setup(self.ECHO,GPIO.IN)

	def getData(self, receiver):
		return Data(self.tipo, receiver,self.sense(), "cm")

	def sense(self):
		GPIO.output(self.TRIG,False)
	#	print "Waiting for sensor to settle"
		time.sleep(0.5)

		GPIO.output(self.TRIG,True)
		time.sleep(0.00001)
		GPIO.output(self.TRIG,False)

		while GPIO.input(self.ECHO)==0:
			pulse_start = time.time()
	
		while GPIO.input(self.ECHO)==1:
			pulse_end = time.time()
	
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17000
		distance = round(distance,2)

		return distance

	def getType(self):
		return self.tipo
		
GPIOSensor.register(Ultrasonic)
