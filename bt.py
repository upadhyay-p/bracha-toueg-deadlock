from mpi4py import MPI
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
terminationTime=None
class Node:
	def __init__(self, id):
		self.id = id
		self.free = False
		self.notified = False
		self.requests = 0
		self.Out = []
		self.In = []
		self.initiator = False

	def addOut(self,u):
		self.Out.append(u)
		self.requests+=1

	def addIn(self,u):
		self.In.append(u)

	def initiate(self):
		self.initiator = True
		self.notify(self.id)

	def checkTermination(self):
		if self.requests==0 and self.free==False:
			self.grant()
		for i in self.Out:
			if i!="DONE":
				return False
		return True
	def allDone(self):
		# print("allDone called,,,,,"+str(self.Out)+"...by P"+str(self.id))
		for i in self.Out:
			if i!="DONE":
				return False
		return True
	def listen(self):
		msg = comm.recv(source=MPI.ANY_SOURCE)
		# print("P"+str(msg[0])+" sent P"+str(self.id)+" msg = "+str(msg))
		self.handleMsg(msg)

	def handleMsg(self,msg):
		sender = msg[0]
		receiver = self.id
		# print(str(self.id)+"<====="+str(msg[0])+" msgRCVD:"+msg[1])

		if msg[1]=="NOTIFY":
			if self.notified==True:
				# print(str(self.id)+"=====>"+str(msg[0])+" msgSENT:DONE")
				comm.send([self.id, "DONE"], dest = sender-1)
				return
			if self.notified==False:
				self.notify(self.id)
			while self.allDone()==False:
				msg = comm.recv()
				self.handleMsg(msg)
			# print("await oberrrrrrrr for P"+str(self.id))
			# print(str(self.id)+"=====>"+str(msg[0])+" msgSENT:DONE")
			comm.send([receiver, "DONE"], dest = sender-1)
		if msg[1]=="GRANT":
			if self.requests>0:
				self.requests-=1
				if self.requests==0:
					# print("iski req ==0 P"+str(self.id))
					self.grant()
				# print(str(self.id)+"=====>"+str(msg[0])+" msgSENT:ACK")
				comm.send([receiver, "ACK"], dest = sender-1)		
			
		if msg[1]=="DONE":
			for i in range(len(self.Out)):
				if self.Out[i]==msg[0]:
					self.Out[i]="DONE"
					break
		if msg[1]=="ACK":
			for i in range(len(self.In)):
				if msg[0]==self.In[i]:
					self.In[i]="ACK"
					break
		
		if msg[1]=="TERMINATE":
			# print("ever here?")
			sys.exit(0)
		# return "CONTINUE"


	def notify(self,sender):
		if self.notified==False:
			self.notified = True
			Out = self.Out
			for i in range(len(Out)):
				if Out[i]!="DONE":
					# print(str(self.id)+"=====>"+str(Out[i])+" msgSENT:NOTIFY")
					comm.send([self.id,"NOTIFY"], dest = Out[i]-1)
				# self.listen()

			if self.requests==0 :
				self.grant()

	def grant(self):
		# print("P"+str(rank+1)+" called grant()")
		self.free = True
		In = self.In
		for i in range(len(In)):
			if In[i]!="ACK":
				# print(str(self.id)+"=====>"+str(In[i])+" msgSENT:GRANT")
				comm.send([self.id,"GRANT"], dest = In[i]-1)
				# self.listen()

nodes={}
file = open("input.txt","r")
lines = file.readlines()
initiator = int(lines[0])
lines = lines[1:]
nodes[rank+1] = Node(rank+1)
for i in lines:
	[u,v] = i.split(" ")
	u = int(u)
	v = int(v)
	if u == rank+1:
		nodes[u].addOut(v)
	elif v == rank+1:
		nodes[v].addIn(u)


if rank+1==initiator:
	nodes[rank+1].initiate()
# else:
# 	nodes[rank+1].listen()

while True:
	nodes[rank+1].listen()
	if rank+1 == initiator and nodes[rank+1].allDone():
		if nodes[initiator].free==True:
			print("***No deadlock***")
		elif nodes[initiator].requests>0:
			print("***Deadlock present***")
		for i in range(comm.Get_size()):
			if i!=rank:
				comm.send([initiator,"TERMINATE"],dest=i)
		break

		# for i in range(comm.Get_size()):
		# 	if i!=rank:
		# 		comm.send([initiator,"TERMINATE"],dest=i)
		
		# break
	# sys.exit(0)
		# while True:
		# 	x = nodes[rank+1].listen()
		# 	print("P"+str(rank+1)+" "+x)
		# 	if x == "TERMINATE":
		# 		break
# while rank+1==initiator:

# if rank==initiator-1:
# 	if nodes[rank+1].allDone():
# 		if nodes[rank+1].free==True:
# 			print("***No deadlock***")
# 		elif nodes[rank+1].requests>0:
# 			print("***Deadlock present***")
# 	else:
# 		print("#####progress:"+str(nodes[rank+1].Out))

file.close()
# print("out of loop P"+str(rank+1))
sys.exit(0)
# sys.exit(0)