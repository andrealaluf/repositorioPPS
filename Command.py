import sys

sys.path.index(0,'/home/fabio/Communicator' )

from messageClass import Message

class Command (Message):
	
	# Constructor
	def __init__(self, receiverID, senderID, priority, timeOut, device, command, value):
		Message.__init__(self, receiverID, senderID, priority, timeOut, device)
		self.command = command
		self.value = value

	def getCommand(self):
		return self.command

	def getValue(self):
		return self.value
	
