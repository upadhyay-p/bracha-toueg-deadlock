from mpi4py import MPI
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

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

	def addOut(self,u):
		self.Out.append(u)
		self.requests+=1

	def addIn(self,u):
		self.In.append(u)

	# def listen(self):
	# 	msg = comm.recv()
	# 	# if msg[1] in ["GRANT", "NOTIFY"]:
	# 	x = self.handleGrantNotify(msg)
	# 	return x

	# # def handleGrantNotify(self,msg):
	# 	sender = msg[0]
	# 	receiver = self.id
	# 	print(str(self.id)+"<====="+str(msg[0])+" msgRCVD:"+msg[1])

	# 	if msg[1]=="NOTIFY":
	# 		if self.notified==False:
	# 			self.notify()
	# 		else:
	# 			print(str(self.id)+"=====>"+str(msg[0])+" msgSENT:DONE")
	# 			comm.send([receiver, "DONE"], dest = sender-1)
	# 	elif msg[1]=="GRANT":
	# 		if self.requests>0:
	# 			self.requests-=1
	# 			if self.free==True or self.requests>0:
	# 				print(str(self.id)+"=====>"+str(msg[0])+" msgSENT:ACK")
	# 				comm.send([receiver, "ACK"], dest = sender-1)		
	# 			else:
	# 				self.grant()
			
	# 	elif msg[1]=="DONE":
	# 		for i in range(len(self.Out)):
	# 			if self.Out[i]==msg[0]:
	# 				self.Out[i]="DONE"
	# 				break
	# 	elif msg[1]=="ACK":
	# 		for i in range(len(self.In)):
	# 			if msg[0]==self.In[i]:
	# 				self.In[i]="ACK"
	# 				break
	# 	elif msg[1]=="TERMINATE":
	# 		return "TERMINATE"
	# 	return "CONTINUE"

	def doneMsg(self):
		for i in range(len(self.Out)):
				if self.Out[i]==msg[0]:
					self.Out[i]="DONE"
					break
	def ackMsg(self):
		for i in range(len(self.In)):
				if msg[0]==self.In[i]:
					self.In[i]="ACK"
					break

	def notify(self):
		self.notified = True
		Out = self.Out
		for i in range(len(Out)):
			if Out[i]!="DONE":
				print(str(self.id)+"=====>"+str(Out[i])+" msgSENT:NOTIFY")
				comm.send([self.id,"NOTIFY"], dest = Out[i]-1)
				# self.listen()
		# for i in range(len(Out)):
			# msg = comm.recv()
			# if msg[1]=="DONE" and msg[0]==Out[i]:
			# 	print(str(self.id)+"<====="+str(msg[0])+" msgRCVD:"+msg[1])
			# 	Out[i]="DONE"
			# else:
			# 	print("P "+str(self.id)+"yahan kabhi-1")
			# 	i=i-1
			# 	if msg[1] in ["GRANT","NOTIFY"]:
			# 		self.handleGrantNotify(msg)
		# if self.requests==0:
		# 	self.grant()

	def grant(self):
		self.free = True
		In = self.In
		for i in range(len(In)):
			if In[i]!="ACK":
				print(str(self.id)+"=====>"+str(In[i])+" msgSENT:GRANT")
				comm.send([self.id,"GRANT"], dest = In[i]-1)
				# self.listen()
		# for i in range(len(In)):
			# msg = comm.recv()
			# if msg[1] == "ACK" and msg[0]==In[i]:
			# 	print(str(self.id)+"<====="+str(msg[0])+" msgRCVD:"+msg[1])
			# 	In[i]="ACK"
			# else:
			# 	print("P "+str(self.id)+"yahan kabhi-2")
			# 	i=i-1
			# 	if msg[1] in ["GRANT","NOTIFY"]:
			# 		self.handleGrantNotify(msg)

nodes={}
file = open("input.txt","r")
lines = file.readlines()
initiator = int(lines[0])
lines = lines[1:]
nodes[rank+1] = Node(rank+1)
if rank+1==initiator:
	nodes[rank+1].setInitiator()
for i in lines:
	[u,v] = i.split(" ")
	u = int(u)
	v = int(v)
	if u == rank+1:
		nodes[u].addOut(v)
	elif v == rank+1:
		nodes[v].addIn(u)

if rank+1 == initiator:
	nodes[initiator].notify()
# 	if nodes[initiator].free==True and nodes[initiator].requests==0:
# 		print("No deadlock")
# 	else:
# 		print("Deadlock present")
# 	for i in range(comm.Get_size()):
# 		if i!=rank:
# 			print("sending TERMINATE to P"+str(i))
# 			comm.send([initiator,"TERMINATE"], i)

while True:
	if rank==initiator-1:
		if nodes[initiator].free==True and nodes[initiator].requests==0:
			print("No deadlock")
			comm.bcast([initiator,"TERMINATE"], root=rank)
			sys.exit(0)
		else:
			print("Deadlock present")
			comm.bcast([initiator,"TERMINATE"], root=rank)
			sys.exit(0)


	msg = comm.recv(source=MPI.ANY_SOURCE)
	if msg[1]=="NOTIFY":
		if nodes[rank+1].notified==True and nodes[rank+1].allDone() and nodes[rank+1].requests==0:
			nodes[rank+1].grant()
		else:
			nodes[rank+1].notify()
		# 
	if msg[1]=="GRANT":
		nodes[rank+1].grant()
		# 
	if msg[1]=="DONE":
		nodes[rank+1].doneMsg()
		# 
	if msg[1]=="ACK":
		nodes[rank+1].ackMsg()
	if msg[1]=="TERMINATE":
		sys.exit(0)
		# 

	# nodes[rank+1].listen()
	# sys.exit(0)
	# while True:
	# 	x = nodes[rank+1].listen()
	# 	print("P"+str(rank+1)+" "+x)
	# 	if x == "TERMINATE":
	# 		break
print("out of loop P"+str(rank+1))