from Message import Message

class Data (Message):
	
	def __init__(self, senderID, receiverID, data, unit):
		Message.__init__(self,senderID, receiverID)
		self.data = data
		self.unit = unit

	def getData(self):
		return self.data

	def getUnit(self):
		return self.unit

