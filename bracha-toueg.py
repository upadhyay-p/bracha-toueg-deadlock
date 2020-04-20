class Node:
	def __init__(self, id):
		self.id = id
		self.free = False
		self.notified = False
		self.requests = 0
		self.Out = []
		self.In = []
		self.initiator = False

	def isDeadlockFree(self):
		for i in self.Out:
			if i is not "DONE":
				print(i)
				return False
		return self.free

	def addOut(self,u):
		self.Out.append(u)
		print("adding outgoing request edge "+str(self.id)+"-"+str(u.id))
		self.requests+=1

	def addIn(self,u):
		self.In.append(u)
		print("adding incoming request edge "+str(self.id)+"-"+str(u.id))
		# pass

	def notify(self,):
		self.notified = True
		for p in self.Out:
			if p is not "DONE":
				self.message(self, p, "NOTIFY")
		if self.requests is 0:
			self.grant()

	def grant(self):
		self.free = True
		print("Freeing "+str(self.id))
		for p in self.In:
			if p is not "ACK":
				self.message(self, p, "GRANT")

	def message(self, sender, reciever , msg):
		if msg is "NOTIFY":
			if reciever.notified is False:
				reciever.notify()
				self.message(reciever, sender, "DONE")
		elif msg is "GRANT":
			if reciever.requests > 0:
				reciever.requests-=1
				self.message(reciever, sender, "ACK")
			if reciever.requests == 0:
				reciever.grant()
				
		elif msg is "DONE":
			for i in range(len(reciever.Out)):
				if reciever.Out[i] == sender:
					reciever.Out[i] = "DONE"
					break
		elif msg is "ACK":
			for i in range(len(reciever.In)):
				if reciever.In[i] is sender:
					reciever.In[i] = "ACK"
					break

# read dependencies from file
file = open("input.txt","r")
lines = file.readlines()
numberOfNodes = int(lines[0])
initiator = int(lines[1])
lines = lines[2:]
dict={}
for i in range(numberOfNodes):
	dict[i+1] = Node(i+1)
	if i+1==initiator:
		dict[i+1].initiator=True

# dict[initiator].setInitiator()
# print(dict[initiator])
for i in lines:
	[u,v] = i.split(" ")
	u = int(u)
	v = int(v)
	dict[u].addOut(dict[v])
	dict[v].addIn(dict[u])
	# print(i)

dict[initiator].notify()

print("Is "+str(initiator)+ " deadlock free? "+ str(dict[initiator].isDeadlockFree()))
# for every node Node object is created
# 