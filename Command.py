from Message import Message

class Command (Message):
	
	# Constructor
	def __init__(self, senderID, receiverID, command,value):
		Message.__init__(self,senderID, receiverID)
		self.command = command
		self.value = value

	def getCommand(self):
		return self.command
	
	def getSenderID(self):
		return self.senderID

	def getValue(self):
		return self.value
	
