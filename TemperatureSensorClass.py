import RPi.GPIO as GPIO
import time
import abc
from GPIOSensor import GPIOSensor
from Data import Data

class HumidityTemperature(GPIOSensor):
	
	def __init__(self, frecuencia, pins):
		GPIOSensor.__init__(self, frecuencia, pins)
		self.tipo = "TEMPERATURE"
		GPIO.setmode(GPIO.BCM) # Usa el sistema de nombramiento BCM - la otra alternativa es BOARD
		self.setGPIOpins()

	def setGPIOpins(self):
		self.OUT = self.pins[0]

	def getData(self, receiver, priority, timeout, device):
		return Data(receiver, self.tipo, priority, timeout, device, self.sense(), "C")

	def sense(self):
		data = []
		 
		GPIO.setup(self.OUT,GPIO.OUT)
		GPIO.output(self.OUT,GPIO.HIGH)
		time.sleep(0.025)
		GPIO.output(self.OUT,GPIO.LOW)
		time.sleep(0.02)
		 
		GPIO.setup(self.OUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		 
		for i in range(0,500):
		    data.append(GPIO.input(self.OUT))
		    
		bit_count = 0
		tmp = 0
		count = 0
		HumidityBit = ""
		TemperatureBit = ""
		crc = ""
		
		# Recepcion de datos 
		try:
			while data[count] == 1:		# Espera por la senal de inicio emitida por el sensor. Cuando se pone en 0 inicia la transmision de datos
				tmp = 1
				count = count + 1
		 
			for i in range(0, 32):
				bit_count = 0
		 
				while data[count] == 0:	# Ceros de la transmision
					tmp = 1
					count = count + 1
		 
				while data[count] == 1:	# Unos de la transmision
					bit_count = bit_count + 1
					count = count + 1
		 
				if bit_count >= 3:
					if i>=0 and i<8:
						HumidityBit = HumidityBit + "1"
					if i>=16 and i<24:
						TemperatureBit = TemperatureBit + "1"
				else:
					if i>=0 and i<8:
						HumidityBit = HumidityBit + "0"
					if i>=16 and i<24:
						TemperatureBit = TemperatureBit + "0"
						
			Temperature = self.bin2dec(TemperatureBit)
			time.sleep(2)
			return Temperature
		except: 
			print "ERR_RANGE"
	
	def bin2dec(self, string_num):
		return str(int(string_num, 2))

	def getType(self):
		print self.tipo
		
GPIOSensor.register(HumidityTemperature)