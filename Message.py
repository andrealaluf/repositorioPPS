class Message (object):
	
	def __init__(self, senderID, receiverID):
		self.senderID = senderID
		self.receiverID = receiverID
		
	def getReceiver(self):
		return self.receiverID
	
