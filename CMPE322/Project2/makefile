all: simulation

simulation: simulation.o
	 g++ -pthread simulation.o -o simulation

simulation.o: 2015400183.cpp
	 g++ -c -pthread 2015400183.cpp -o simulation.o
     
clean:
	 rm simulation.o simulation

