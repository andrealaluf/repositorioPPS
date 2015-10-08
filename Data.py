from Message import Message

class Data (Message):
	
	def __init__(self, receiverID, senderID, priority, timeOut, device, command, value):
		Message.__init__(self, receiverID, senderID, priority, timeOut, device)
		self.data = data
		self.unit = unit

	def getData(self):
		return self.data

	def getUnit(self):
		return self.unit

