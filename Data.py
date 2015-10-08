import sys

sys.path.insert(0,'/home/fabio/Communicator')

from messageClass import Message

class Data (Message):
	
	def __init__(self, receiverID, senderID, priority, timeOut, device, data, unit):
		Message.__init__(self, receiverID, senderID, priority, timeOut, device)
		self.data = data
		self.unit = unit

	def getData(self):
		return self.data

	def getUnit(self):
		return self.unit

