import abc

class Sensor(object):
	__metaclass__ = abc.ABCMeta

	def __init__(self, frecuencia):
		self.frecuencia = frecuencia	# frecuencia con la que se toman dato
		self.senseFlag = False				

	def setFrequency(self, frecuency):
		self.frecuencia = float(frecuency)

	def getFrequency(self):
		return self.frecuencia

	def setSenseFlag(self,value):
		self.senseFlag = value

	def getSenseFlag(self):
		return self.senseFlag
			  	
	# def getCommand(self, command, value):
	# 	if command == 'SENSE':
	# 		self.sense()
	# 	elif command == 'SETFR':
	# 		self.setFrequency(value)
	# 	else:
	# 		self.clearSensor()
	
# ---------------- Metodos abstractos --------------------
	
	@abc.abstractmethod	
	def getData(self, sender, data, unit):
		pass
	@abc.abstractmethod
	def clearSensor(self):
		""" Elimina sensor """
		pass
	
	@abc.abstractmethod
	def sense(self):
		""" Realiza una lectura del sensor """
		pass

	@abc.abstractmethod
	def getType(self):
		""" Retorna el tipo de sensor """
	


