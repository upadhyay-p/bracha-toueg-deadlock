from mpi4py import MPI
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nodes = {}
class Node:
	def __init__(self, id):
		self.id = id
		self.free = False
		self.notified = False
		self.requests = 0
		self.Out = []
		self.In = []
		self.initiator = False

	def setInitiator(self):
		self.initiator = True

	def checkAllDone(self):
		for i in self.Out:
			if i != "DONE":
				return False
		return True

	def isDeadlockFree(self):
		return self.free==True

	def addOut(self,u):
		self.Out.append(u)
		# print("adding outgoing request edge "+str(self.id)+"-"+str(u.id))
		self.requests+=1

	def addIn(self,u):
		self.In.append(u)

	def notify(self):
		print("Process"+str(self.id)+" function call notify()")
		if self.notified==True:
			return
		self.notified = True
		for p in range(len(self.Out)):
			if self.Out[p] != "DONE":
				print("Sending NOTIFY msg from "+str(self.id)+" to "+str(self.Out[p]))
				comm.send([self.id,"NOTIFY"], dest=self.Out[p]-1)
				msg = comm.recv()
				if msg == "DONE":
					print("DONE recvd")
					self.Out[p] = "DONE"
				# self.message(self, p, "NOTIFY")
		if self.requests == 0:
			self.grant()

	def grant(self):
		print("Process"+str(self.id)+" function call grant()")
		self.free = True
		# print("Freeing "+str(self.id))
		for p in range(len(self.In)):
			if self.In[p] != "ACK":
				print("Sending GRANT msg from "+str(self.id)+" to "+str(self.In[p]))
				comm.send([self.id,"GRANT"], dest=self.In[p]-1) 
				msg = comm.recv()
				if msg == "ACK":
					print("ACK rcvd")
					self.In[p] = "ACK"



file = open("input.txt","r")
lines = file.readlines()
initiator = int(lines[0])
lines = lines[1:]
nodes[rank+1] = Node(rank+1)
# print("node object created for process"+str(rank+1)+"==="+str(nodes))
if rank+1==initiator:
	# print("Process"+str(rank+1)+" set as initiator")
	nodes[rank+1].setInitiator()
for i in lines:
	[u,v] = i.split(" ")
	u = int(u)
	v = int(v)
	if u == rank+1:
		# print("Adding out edge "+str(u)+"-"+str(v)+" for Process"+str(rank+1))
		nodes[u].addOut(v)
	elif v == rank+1:
		# print("Adding in edge"+str(u)+"-"+str(v)+" for Process"+str(rank+1))
		nodes[v].addIn(u)

# print("Process-"+str(rank+1)+"free="+str(nodes[rank+1].free))
# print("Process-"+str(rank+1)+"notified="+str(nodes[rank+1].notified))
# print("Process-"+str(rank+1)+"requests="+str(nodes[rank+1].requests))
# print("Process-"+str(rank+1)+"Out="+str(nodes[rank+1].Out))
# print("Process-"+str(rank+1)+"In="+str(nodes[rank+1].In))
# print("Process-"+str(rank+1)+"initiator="+str(nodes[rank+1].initiator))



if rank+1 == initiator:
	nodes[rank+1].notify()
	loopVar=True
else:
	msg = None
	loopVar = True

# while loopVar:
# 	# print("Process "+str(rank+1))
# 	if rank==initiator-1 and nodes[initiator].checkAllDone()==True:
# 		# and nodes[initiator].checkAllDone==True
# 		print("checkall: "+str(nodes[initiator].Out))
# 		# comm.send(loopVar, dest=0)
# 		# comm.bcast(loopVar, root=0)
# 		break;
# 	# loopVar = comm.bcast(loopVar, root=0)
# 	if nodes[rank+1].checkAllDone():
# 		break
while True:
	msg = comm.recv()

		# print("LoopVar= "+str(loopVar)+" ||P"+str(rank+1)+" In while loop msg is "+msg[1]+" from process "+str(msg[0]))
		
		

	if msg[1] == "NOTIFY":
		# print("phasa "+str(rank+1))
		if (rank+1) in nodes:
			if nodes[rank+1].notified == False:
				nodes[rank+1].notify()
				print("Sending DONE msg to "+str(msg[0])+" from "+str(rank+1))
				comm.send([rank+1,"DONE"],dest=msg[0]-1)
	elif msg[1] == "GRANT":
		if (rank+1) in nodes:
			if nodes[rank+1].requests>0:
				nodes[rank+1].requests = nodes[rank+1].requests-1
				if nodes[rank+1].requests == 0:
					nodes[rank+1].grant()
			print("Sending ACK msg to "+str(msg[0])+" from "+str(rank+1))
			comm.send([rank+1,"ACK"], dest=msg[0]-1)
			
	# elif msg[1] == "DONE":
	# 	print("DONE recvd")
	# 	if (rank+1) in nodes:
	# 		for i in range(len(nodes[rank+1].Out)):
	# 			print(".")
	# 			if nodes[rank+1].Out[i] == msg[0]:
	# 				nodes[rank+1].Out[i] = "DONE"
	# 				print("for P"+str(rank+1)+" P"+str(msg[0])+" is DONE")
	# 				break
	# elif msg[1] == "ACK":
	# 	print("ACK recvd")
	# 	if (rank+1) in nodes:
	# 		for i in range(len(nodes[rank+1].In)):
	# 			print(".")
	# 			if nodes[rank+1].In[i] == msg[0]:
	# 				nodes[rank+1].In[i] = "ACK"
	# 				break
	# else:
	# 	break

print("out of loop - p"+str(rank+1))

if rank == initiator-1:
	ans = nodes[initiator].isDeadlockFree()
	print("DEADLOCK FREE???"+str(ans))
	sys.exit(0)

# comm.send(data, dest=1, tag=11)

# data = comm.recv(source=0, tag=11)

# 	def message(self, sender, reciever , msg):
# 		if msg is "NOTIFY":
# 			if reciever.notified is False:
# 				reciever.notify()
# 			self.message(reciever, sender, "DONE")

# 		elif msg is "GRANT":
# 			if reciever.requests > 0:
# 				reciever.requests-=1
# 				self.message(reciever, sender, "ACK")
# 			if reciever.requests == 0:
# 				reciever.grant()
				
# 		elif msg is "DONE":
# 			for i in range(len(reciever.Out)):
# 				if reciever.Out[i] == sender:
# 					reciever.Out[i] = "DONE"
# 					break

# 		elif msg is "ACK":
# 			for i in range(len(reciever.In)):
# 				if reciever.In[i] is sender:
# 					reciever.In[i] = "ACK"
# 					break