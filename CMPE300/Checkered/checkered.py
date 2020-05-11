#Name: Baran Deniz Korkmaz
#Compilation Status:Compiling
#Working Status:Working
#
#Implementation Details: Periodic & Checkered Version
#Run in Terminal: mpirun -np [n] --oversubscribe python3 2015400183.py [input.txt] [output.txt] [T]
#

#Below are the packages utilized for the project.
from mpi4py import MPI
import sys
import math
import numpy as np

#Defining some constant variables that are specified by the description.
MAP_SIZE=360
INPUT_FILE=sys.argv[1]
OUTPUT_FILE=sys.argv[2]
ITERATIONS=int(sys.argv[3])

#Initialize MPI environment and create global variables that will be used througout the program.
MASTER_PROCESS=0
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()
num_of_workers=size-1
size_sqrt=int(math.sqrt(num_of_workers))

#get_row_num and get_col_num functions returns the row and column indexes of a given process id which is assigned to a specific part of the grid.
def get_row_num(rank_):
    return int(((rank_-1)/size_sqrt)+1)

def get_col_num(rank_):
    return (rank_-1)%size_sqrt+1

#Below are the functions which return the neighbor ids of a given process id which are assigned to the neighbor regions of that process.
def get_left(rank_):
    row_num_i=get_row_num(rank_)
    col_num_i=get_col_num(rank_)
    col_num_i=col_num_i - 1
    if(col_num_i < 1):
        col_num_i=col_num_i+size_sqrt
    return get_process_id(row_num_i,col_num_i)

def get_right(rank_):
    row_num_i = get_row_num(rank_)
    col_num_i = get_col_num(rank_)
    col_num_i = col_num_i + 1
    if (col_num_i > size_sqrt):
        col_num_i = col_num_i - size_sqrt
    return get_process_id(row_num_i, col_num_i)

def get_top(rank_):
    row_num_i = get_row_num(rank_)
    col_num_i = get_col_num(rank_)
    row_num_i = row_num_i - 1
    if (row_num_i < 1):
        row_num_i = row_num_i + size_sqrt
    return get_process_id(row_num_i, col_num_i)

def get_bottom(rank_):
    row_num_i = get_row_num(rank_)
    col_num_i = get_col_num(rank_)
    row_num_i = row_num_i + 1
    if (row_num_i > size_sqrt):
        row_num_i = row_num_i - size_sqrt
    return get_process_id(row_num_i, col_num_i)

def get_top_left(rank_):
    return get_left(get_top(rank_))

def get_top_right(rank_):
    return get_right(get_top(rank_))

def get_bottom_left(rank_):
    return get_left(get_bottom(rank_))

def get_bottom_right(rank_):
    return get_right(get_bottom(rank_))

#The id of a process can be calculated by using its row and column indexes. This function operates as a supplementer for the functions that are defined above.
def get_process_id(row,col):
    return int((row-1)*size_sqrt+col)

#Master process communicates with all worker processes via this function. The function takes two arguments:
#The first argument is the 2D array which contains our grid.
#The second argument is a string which determines if the master will make a send or receive operation.
#In case of an invalid arg entry, the program returns the error code of -1.
def communicate_workers(map,cmd):
    for i in range(1, num_of_workers + 1):
        row_num = get_row_num(i)
        col_num = get_col_num(i)
        row_from = int(MAP_SIZE / size_sqrt * (row_num - 1))
        row_to = int(MAP_SIZE / size_sqrt * (row_num))
        col_from = int(MAP_SIZE / size_sqrt * (col_num - 1))
        col_to = int(MAP_SIZE / size_sqrt * (col_num))
        if(cmd=="send"):
            temp_array = map[row_from:row_to, col_from:col_to]
            comm.send(temp_array, dest=i, tag=i)
        elif(cmd=="recv"):
            worker_result = comm.recv(source=i, tag=MASTER_PROCESS)
            map[row_from:row_to, col_from:col_to] = worker_result
        else:
            return(-1)

#The worker process communicates with its neighbors via this function. The function takes two arguments:
#The first argument is the 2D array which contains the subportion of the worker process.
#The second argument is a string which determines whether the communication process will be carried out with the neighbors that have the same modulo%2 value or not.
#In case of an invalid arg entry, the program returns the error code of -1.
def send_neighbors(slice,cmd):
    if(cmd=="diff"):#Includes every direction except send top & bottom
        comm.send(slice[:, 0], dest=get_left(rank), tag=get_left(rank))  # send left
        comm.send(slice[:, len(slice) - 1], dest=get_right(rank), tag=get_right(rank))  # send right
        comm.send(slice[0, 0], dest=get_top_left(rank), tag=get_top_left(rank))  # send top left
        comm.send(slice[0, len(slice) - 1], dest=get_top_right(rank), tag=get_top_right(rank))  # send top right
        comm.send(slice[len(slice) - 1, 0], dest=get_bottom_left(rank), tag=get_bottom_left(rank))  # send bottom left
        comm.send(slice[len(slice) - 1, len(slice) - 1], dest=get_bottom_right(rank), tag=get_bottom_right(rank))  # send bottom right
    elif(cmd=="same"):#Includes send top & bottom
        comm.send(slice[0, :], dest=get_top(rank), tag=get_top(rank))  # send top
        comm.send(slice[len(slice) - 1, :], dest=get_bottom(rank), tag=get_bottom(rank))  # send bottom
    else:
        return(-1)

if __name__ == "__main__":
    if rank==0:#Master process operates inside of this block.
        #Master process read the input file and gets its content into a 2D array of size 360x360.
        map=np.genfromtxt(INPUT_FILE,delimiter=" ",dtype=int)

        #Master process sends the map portions into each processes which they should be assigned to.
        communicate_workers(map,"send")

        #Master process receives the final array subportions from the worker processes and inserts them into the proper places in the map.
        communicate_workers(map,"recv")

        #Since master has received the results and properly inserted them into the map, it finally writes the content into the output file.
        np.savetxt(fname=OUTPUT_FILE, X=map.astype(int), fmt='%.0f')

    else:#Worker processes operates inside of this block, since they have a nonzero id number.
        row_num_process = get_row_num(rank)
        col_num_process = get_col_num(rank)
        #Worker process receives the subportion from the 2D array of map and writes the content into the 2D array 'slice'.
        slice=comm.recv(source=MASTER_PROCESS,tag=rank)
        #slice_size=int(MAP_SIZE/size_sqrt)
        for i in range(ITERATIONS): #Iterations are implemented.
            #Odd-ranked processes carry out send&receive operations.
            if rank%2==1:
                #In order to prevent the deadlocks, the send&recv operations must be arranged.
                #Therefore in the case of odd-ranked processes, the process first sends into even numbered neighbors.
                send_neighbors(slice,"diff")
                # The processes with odd-rank & odd row indexes carry out send&receive to/from top/bottom processes so as to prevent deadlocks.
                if(row_num_process%2==1):
                    send_neighbors(slice,"same")
                    from_bottom = comm.recv(source=get_bottom(rank), tag=rank)  # recv bottom
                    from_top=comm.recv(source=get_top(rank),tag=rank) #recv top
                else:# The processes with even row indexes carry out send&receive to/from top/bottom processes so as to prevent deadlocks.
                    from_bottom = comm.recv(source=get_bottom(rank), tag=rank)  # recv bottom
                    from_top = comm.recv(source=get_top(rank), tag=rank)  # recv top
                    send_neighbors(slice,"same")
                #The odd-ranked process now recieves from the even numbered neighbors.
                from_bottom_right = comm.recv(source=get_bottom_right(rank), tag=rank)  # recv bottom right
                from_bottom_left = comm.recv(source=get_bottom_left(rank), tag=rank)  # recv bottom left
                from_top_right = comm.recv(source=get_top_right(rank), tag=rank)  # recv top right
                from_top_left = comm.recv(source=get_top_left(rank), tag=rank)  # recv top left
                from_right = comm.recv(source=get_right(rank), tag=rank)  # recv right
                from_left=comm.recv(source=get_left(rank),tag=rank) #recv left
            else:#Even-numbered processes carry out send&receive operations as explained above but in an opposite direction.
                from_bottom_right = comm.recv(source=get_bottom_right(rank), tag=rank)  # recv bottom right
                from_bottom_left = comm.recv(source=get_bottom_left(rank), tag=rank)  # recv bottom left
                from_top_right = comm.recv(source=get_top_right(rank), tag=rank)  # recv top right
                from_top_left = comm.recv(source=get_top_left(rank), tag=rank)  # recv top left
                from_right = comm.recv(source=get_right(rank), tag=rank)  # recv right
                from_left = comm.recv(source=get_left(rank), tag=rank)  # recv left

                if(row_num_process%2==1):
                    send_neighbors(slice,"same")
                    from_bottom = comm.recv(source=get_bottom(rank), tag=rank)  # recv bottom
                    from_top=comm.recv(source=get_top(rank),tag=rank) #recv top
                else:
                    from_bottom = comm.recv(source=get_bottom(rank), tag=rank)  # recv bottom
                    from_top = comm.recv(source=get_top(rank), tag=rank)  # recv top
                    send_neighbors(slice,"same")

                send_neighbors(slice,"diff")

            #In order to carry out game of life computations easier, the subportions received from the neighbors surrounds the slice of the worker process.
            temp_array=np.zeros((len(slice)+2,len(slice)+2),dtype=int)
            temp_array[1:len(slice)+1,1:len(slice)+1]=slice
            temp_array[0,1:len(slice)+1]=from_top
            temp_array[len(slice)+1,1:len(slice)+1]=from_bottom
            temp_array[1:len(slice)+1,0]=from_left
            temp_array[1:len(slice)+1,len(slice)+1]=from_right
            temp_array[0,0]=from_top_left
            temp_array[0,len(slice)+2-1]=from_top_right
            temp_array[len(slice)+2-1,0]=from_bottom_left
            temp_array[len(slice)+2-1,len(slice)+2-1]=from_bottom_right

            #Game of life computations occur.
            for i in range(1,len(slice)+1):
                for j in range(1,len(slice)+1):
                    sum=int(temp_array[i-1,j-1])+int(temp_array[i-1,j])+int(temp_array[i-1,j+1])+int(temp_array[i,j-1])+int(temp_array[i,j+1])+int(temp_array[i+1,j-1])+int(temp_array[i+1,j])+int(temp_array[i+1,j+1])
                    if(sum<2 or sum>3):
                        slice[i-1,j-1]=0
                    else:
                        if(sum==3):
                            slice[i-1,j-1]=1 #The computations are stored in the slice array which is the permanent subportion of the process.

        #Since all iterations have been done, the process sends its final subportion into the master process.
        comm.send(slice,dest=MASTER_PROCESS,tag=MASTER_PROCESS)
