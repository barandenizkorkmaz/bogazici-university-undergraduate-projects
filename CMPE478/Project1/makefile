all: main

main: main.o
	 g++ main.o -o main -fopenmp

main.o: main.cpp
	 g++ -c main.cpp -o main.o -fopenmp

clean:
	 rm main.o main

