from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank==0:
	for i in range(3):
		comm.send("Hey",1)
	data = comm.recv()
	print(data)
else:
	for i in range(5):
		print("waiting")
		var = comm.recv()
		print(var)
	comm.send("rcvd",0)