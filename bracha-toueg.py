class Node:
	def __init__(self, id):
		self.id = id
		self.free = False
		self.notified = False
		self.requests = 0
		self.Out = []
		self.In = []
		self.initiator = False

	def setInitiator():
		self.initiator = True

	def isDeadlockFree():
		return free

	def addOut(u):
		Out.append(u)
		requests+=1
		# pass

	def addIn(u):
		In.append(u)
		# pass

	def notify():
		notified = True
		for p in Out:
			message(self, p, "NOTIFY")
		if requests is 0:
			grant()
		# await done msgs
		pass

	def grant():
		free = True
		for p in In:
			message(self, p, "GRANT")
		pass

	def message(sender, reciever , msg):
		if msg is "NOTIFY":
			if reciever.notified is False:
				reciever.notify()
			message(reciever, sender, "DONE")
		elif msg is "GRANT":
			if requests > 0:
				requests-=1
				if requests == 0:
					receiver.grant()
			message(reciever, sender, "ACK")
		elif msg is "DONE":
			pass
		elif msg is "ACK":
			pass
		# pass

# read dependencies from file
# for every node Node object is created
# 