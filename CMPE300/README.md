# CMPE300 - Analysis of Algorithms
| Term | Instructor |
| --- | --- |
| Fall 2019  | Tunga Güngör  |

In the project, we implement the Game of Life by using `MPI` (Message Passing
Interface). We are asked to read an input file which constitutes the initial state
of a grid of size 360x360 where each cell represents a state. The cells can take
two values which are 0 and 1. The value of zero implies no existence, whereas
the value of 1 implies a life. The state of the grid at time t depends on the
state of the grid at time t-1. We are aiming at writing the final state of the
grid into an output file after T iterations have been carried out by using parallel
computing.
The project can be implemented by two versions based on the Interconnection Network Architecture. The first one is Split version whereby the processes form a 1D-Mesh, whereas the second one is Checkered version whereby the processes form a 2D-Mesh to communicate. Plus, based on the design of grid boundaries, the project is divided into two options as well: Cutoff and Periodic. In my repository, you will be able to find both Split and Checkered versions with Periodic Grid Boundaries, since I implemented both versions until the deadline of the project. You can find more detailed information about the project in the description added. 
Before running the projects, make sure that you have installed Open MPI. You can find a detailed documentation about how to install Open-MPI, thanks to Mehmet Utkan Gezer who was the teaching assistant as I was taking CMPE 300.
Plus, you can find two testcases in the Testcases folder which are rand and gliders. 

### [Version 1: Split](/CMPE300/Split) `C++`
```bash
# A source code written in C++, say 'main.cpp', can be compiled into the executable 'main' with the following:
mpic++ main.cpp -o main

# A compiled MPI program 'main', can be run with the following:
mpirun -np [M] --oversubscribe ./main [Input.txt] [Output.txt] [T]

#[M]: Number of Processors
#[Input.txt]: The input file.
#[Output.txt]: The output file.
#[T]: The number of Iterations.

# Exp: Run it with 5 processors (1 master, 4 worker processors):
mpirun -np 5 --oversubscribe ./main rand.txt randout.txt 20
```

### [Version 2: Checkered](/CMPE300/Checkered) `Python`
```bash
# To run the program: Make sure that the necessary packages which are math, numpy,and mpi4py are provided.
mpirun -np [M] --oversubscribe python3 main.py [Input.txt] [Output.txt] [T]

#[M]: Number of Processors
#[Input.txt]: The input file.
#[Output.txt]: The output file.
#[T]: The number of Iterations.

# Exp: Run it with 145 processors (1 master, 144 worker processors):
mpirun -np 145 --oversubscribe python3 main.py ./main gliders.txt glidersout.txt 30
```
