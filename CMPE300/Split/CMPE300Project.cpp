#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include <istream>
#include <sstream>
#include <string>
#include <iostream>
#include <vector>

#define MASTER_PROCESS 0
#define MAP_SIZE 360
using namespace std;

void printArray(int* arg,int row,int col);
int **alloc_2d_int(int rows, int cols);
int ITERATIONS=0;

int get_process(int rank,int num_of_workers,string cmd){
    int result;
    if(cmd=="Bottom"){
        result=(rank+1);
        if(result>num_of_workers){
            result=1;
        }
    }
    else if(cmd=="Above"){
        result=(rank-1);
        if(result==0){
            result=num_of_workers;
        }
    }
    return result;
}

int main(int argc, char** argv) {
    //Declare global variables.
    ITERATIONS=stoi(argv[3]);

    // Initialize the MPI environment
    MPI_Init(NULL, NULL);
    // Find out rank, size
    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);
    int num_of_workers=world_size-1;
    
    if(rank==0){
        cout << "You have entered " << argc
             << " arguments:" << "\n";

        for (int i = 0; i < argc; ++i)
            cout << argv[i] << "\n";

        ifstream inFile(argv[1]);
        if(!inFile){
            cout << "inFile not found!" << endl;
            MPI_Finalize();
            return -1;
        }

        int** map=alloc_2d_int(MAP_SIZE,MAP_SIZE);

        string line;
        for (int i=0;i<MAP_SIZE;i++){
            getline(inFile,line);
            istringstream iss(line);

            for(int j=0;j<MAP_SIZE;j++){
                int cur;
                iss >> cur;
                map[i][j]=cur;
            }
        }

        inFile.close();

        int buffer_size=MAP_SIZE/num_of_workers*MAP_SIZE;
        for(int c=1;c<=num_of_workers;c++){
            MPI_Send(&(map[(c-1)*MAP_SIZE/num_of_workers][0]),buffer_size,MPI_INT,c,rank,MPI_COMM_WORLD);
        }
        MPI_Barrier(MPI_COMM_WORLD);
        for(int it=1;it<=ITERATIONS;it++){
            MPI_Barrier(MPI_COMM_WORLD);
            MPI_Barrier(MPI_COMM_WORLD);
            MPI_Barrier(MPI_COMM_WORLD);
        }
        for(int i=1;i<=num_of_workers;i++){
            MPI_Recv(&(map[(i-1)*(MAP_SIZE/num_of_workers)][0]),MAP_SIZE/num_of_workers*MAP_SIZE,MPI_INT,i,i,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
        }
        MPI_Barrier(MPI_COMM_WORLD);
        //Write into output file.
        ofstream outFile(argv[2]);
        if(!outFile){
            cout << "inFile could not be opened!" << endl;
            MPI_Finalize();
            return -1;
        }
        for(int i=0;i<MAP_SIZE;i++){
            for(int j=0;j<MAP_SIZE;j++){
                outFile << map[i][j] << " ";
            }
            outFile << endl;
        }

        outFile.close();
        MPI_Barrier(MPI_COMM_WORLD);
    }
    else{
        int row=MAP_SIZE/num_of_workers;
        int** worker_slice=alloc_2d_int(MAP_SIZE/num_of_workers,MAP_SIZE);
        int* fromAbove=(int *) malloc(MAP_SIZE*sizeof(int));
        int* fromBottom=(int *) malloc(MAP_SIZE*sizeof(int));
        int** temp_worker_slice=alloc_2d_int(row,MAP_SIZE);

        MPI_Recv(&(worker_slice[0][0]),MAP_SIZE/num_of_workers*MAP_SIZE,MPI_INT,MASTER_PROCESS,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
        MPI_Barrier(MPI_COMM_WORLD);

        for(int it=1;it<=ITERATIONS;it++) {
            if (rank % 2 == 1) {
                MPI_Send(&(worker_slice[MAP_SIZE / num_of_workers - 1][0]), MAP_SIZE, MPI_INT, get_process(rank,num_of_workers,"Bottom"), rank,
                         MPI_COMM_WORLD);//send(bottom)
                MPI_Recv(&(fromBottom[0]), MAP_SIZE, MPI_INT, get_process(rank,num_of_workers,"Bottom"), get_process(rank,num_of_workers,"Bottom"), MPI_COMM_WORLD,
                         MPI_STATUS_IGNORE);//recv(bottom)
            } else {
                MPI_Recv(&(fromAbove[0]), MAP_SIZE, MPI_INT, get_process(rank,num_of_workers,"Above"), get_process(rank,num_of_workers,"Above"), MPI_COMM_WORLD,
                         MPI_STATUS_IGNORE);//recv(above)
                MPI_Send(&(worker_slice[0][0]), MAP_SIZE, MPI_INT, get_process(rank,num_of_workers,"Above"), rank, MPI_COMM_WORLD);//send(above)
            }
            MPI_Barrier(MPI_COMM_WORLD);
            if (rank % 2 == 1) {
                MPI_Send(&(worker_slice[0][0]), MAP_SIZE, MPI_INT, get_process(rank,num_of_workers,"Above"), rank, MPI_COMM_WORLD);//send(above)
                MPI_Recv(&(fromAbove[0]), MAP_SIZE, MPI_INT, get_process(rank,num_of_workers,"Above"), get_process(rank,num_of_workers,"Above"), MPI_COMM_WORLD,
                         MPI_STATUS_IGNORE);//recv(above)
            } else {
                MPI_Recv(&(fromBottom[0]), MAP_SIZE, MPI_INT, get_process(rank,num_of_workers,"Bottom"), get_process(rank,num_of_workers,"Bottom"), MPI_COMM_WORLD,
                         MPI_STATUS_IGNORE);//recv(bottom)
                MPI_Send(&(worker_slice[MAP_SIZE / num_of_workers - 1][0]), MAP_SIZE, MPI_INT, get_process(rank,num_of_workers,"Bottom"), rank,
                         MPI_COMM_WORLD);//send(bottom)
            }
            MPI_Barrier(MPI_COMM_WORLD);
            /*
             * Game of Life Computations
             */
            int nw, n, ne, w, e, sw, s, se;
            int sum = 0;
            for (int x = 0; x < row; x++) //for each row
            {
                for (int y = 0; y < MAP_SIZE; y++) //for each column
                {
                    if (x == 0 && y == 0) { //upper-left cell
                        nw = fromAbove[MAP_SIZE - 1];n = fromAbove[0];ne = fromAbove[1];w = worker_slice[x][MAP_SIZE - 1];e = worker_slice[x][y + 1];sw = worker_slice[x + 1][MAP_SIZE - 1];s = worker_slice[x + 1][y];se = worker_slice[x + 1][y + 1];
                    } else if (x == 0 && y == MAP_SIZE - 1) { //upper-right cell
                        nw = fromAbove[MAP_SIZE - 1 - 1];n = fromAbove[MAP_SIZE - 1];ne = fromAbove[0];w = worker_slice[x][y - 1];e = worker_slice[x][0];sw = worker_slice[x + 1][y - 1];s = worker_slice[x + 1][y];se = worker_slice[x + 1][0];
                    } else if (x == row - 1 && y == 0) { //lower-left cell
                        nw = worker_slice[x - 1][MAP_SIZE - 1];n = worker_slice[x - 1][y];ne = worker_slice[x - 1][y + 1];w = worker_slice[x][MAP_SIZE - 1];e = worker_slice[x][y + 1];sw = fromBottom[MAP_SIZE - 1];s = fromBottom[0];se = fromBottom[1];
                    } else if (x == row - 1 && y == MAP_SIZE - 1) { //lower-right cell
                        nw = worker_slice[x - 1][y - 1];n = worker_slice[x - 1][y];ne = worker_slice[x - 1][0];w = worker_slice[x][y - 1];e = worker_slice[x][0];sw = fromBottom[MAP_SIZE - 1 - 1];s = fromBottom[MAP_SIZE - 1];se = fromBottom[0];
                    } else // not corner cells
                    {
                        if (y == 0) { // leftmost line, not corner
                            nw = worker_slice[x - 1][MAP_SIZE - 1];n = worker_slice[x - 1][y];ne = worker_slice[x - 1][y + 1];w = worker_slice[x][MAP_SIZE - 1];e = worker_slice[x][y + 1];sw = worker_slice[x + 1][MAP_SIZE - 1];s = worker_slice[x + 1][y];se = worker_slice[x + 1][y + 1];
                        } else if (y == MAP_SIZE - 1) { //rightmost line, not corner
                            nw = worker_slice[x - 1][y - 1];n = worker_slice[x - 1][y];ne = worker_slice[x - 1][0];w = worker_slice[x][y - 1];e = worker_slice[x][0];sw = worker_slice[x + 1][y - 1];s = worker_slice[x + 1][y];se = worker_slice[x + 1][0];
                        } else if (x == 0) { //uppermost line, not corner
                            nw = fromAbove[y - 1];n = fromAbove[y];ne = fromAbove[y + 1];w = worker_slice[x][y - 1];e = worker_slice[x][y + 1];sw = worker_slice[x + 1][y - 1];s = worker_slice[x + 1][y];se = worker_slice[x + 1][y + 1];
                        } else if (x == row - 1) { //lowermost line, not corner
                            nw = worker_slice[x - 1][y - 1];n = worker_slice[x - 1][y];ne = worker_slice[x - 1][y + 1];w = worker_slice[x][y - 1];e = worker_slice[x][y + 1];sw = fromBottom[y - 1];s = fromBottom[y];se = fromBottom[y + 1];
                        } else { //general case, any cell within
                            nw = worker_slice[x - 1][y - 1];n = worker_slice[x - 1][y];ne = worker_slice[x - 1][y + 1];w = worker_slice[x][y - 1];e = worker_slice[x][y + 1];sw = worker_slice[x + 1][y - 1];s = worker_slice[x + 1][y];se = worker_slice[x + 1][y + 1];
                        }
                    }
                    sum = nw + n + ne + w + e + sw + s + se;
                    //Set the new value of a cell.
                    if (sum<2 || sum>3) {
                        temp_worker_slice[x][y] = 0;
                    } else {
                        if(sum==2){
                            temp_worker_slice[x][y] = worker_slice[x][y];
                        }
                        else{
                            temp_worker_slice[x][y] = 1;
                        }
                    }
                }
            }

            for (int x = 0; x < row; x++)
                for (int y = 0; y < MAP_SIZE; y++)
                    worker_slice[x][y] = temp_worker_slice[x][y];


            MPI_Barrier(MPI_COMM_WORLD);
        }//End of an Iteration

        //Since we have completed every iteration, it's time to send the subportions of the workers back into the master process.
        MPI_Send(&(worker_slice[0][0]),MAP_SIZE/num_of_workers*MAP_SIZE,MPI_INT,MASTER_PROCESS,rank,MPI_COMM_WORLD);

        //Wait until master receives.
        MPI_Barrier(MPI_COMM_WORLD);

        //Wait master writing into the output file.
        MPI_Barrier(MPI_COMM_WORLD);
    }

    //Finalize
    MPI_Finalize();
}

void printArray(int* arg,int row,int col){
    for(int i=0;i<row;i++){
        for(int j=0;j<col;j++){
            cout << *((arg+i*col) + j)<<" ";
        }
        cout << endl;
    }
}

int **alloc_2d_int(int rows, int cols) {
    int *data = (int *)malloc(rows*cols*sizeof(int));
    int **array= (int **)malloc(rows*sizeof(int*));
    for (int i=0; i<rows; i++)
        array[i] = &(data[cols*i]);

    return array;
}
