Compilation & Execution
A. Compilation
>> g++ -c main.cpp -o main.o -fopenmp
>> g++ main.o -o main -fopenmp

B. Execution
>> ./main [M] [CHUNK_SIZE] [--primes (Optional)]

IMPORTANT NOTES:
1. Make sure that M is greater than or equal to 10.
2. The last argument is optional.
3. In case of an invalid argument passing, the program will notify the user as follows:
 

>> Please enter valid arguments: [M (>=10)] [CHUNK_SIZE] (Optional: [--primes])

4. You should not have any other file named "output.csv" in the directory you are running the program.
5. Chunk size must be valid.

** Please inform me in case of an error in compilation/execution, since I have no experience in using MacOSX.
