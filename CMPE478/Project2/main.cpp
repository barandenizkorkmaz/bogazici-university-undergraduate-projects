#include <iostream>
#include "mpi.h"
#include <cmath>
#include <ctype.h>

using namespace std;

double* grid;
double *ghost_grid;
double* actual_grid;

double* left_slice;
double* right_slice;
double* front_slice;
double* behind_slice;
double* top_slice;
double* down_slice;

int N, SIZE, grid_size, ghost_grid_size;
int proc_num, comm_size,comm_size_cube_root;
int x,y,z;
int x_min,x_max,y_min,y_max,z_min,z_max;
int left_neighbor,right_neighbor,front_neighbor,behind_neighbor,top_neighbor,down_neighbor;
double epsilon = pow(10,-5);
double diff = 0.0;
double my_diff = 0.0;
int iteration = 1;

bool isPrint = false;

double u(double x,double y,double z);
double f(double x,double y,double z);
int mod(int number,int modulo);
int get_actual_boundary(int proc_num, char dim);
int get_proc_index(int proc_num, char dim);
int get_proc_num(int x,int y,int z);
int get_neighbor(int proc_num,char where);
bool is_boundary(int i,int j,int k);
bool arg_check(int argc,char** argv);
bool legal_int(char *str);

void print_array(double *arr,int X,int Y,int Z); //for testing purposes
void initialize_grid();
void initialize_actual_grid();
void form_ghost_grid();
void jacobi(double *grid,double *ghost_grid);
double compute_diff();
double compute_final_diff();
void initialize_actual_cube(double* cube);
void deallocate_memory();

int main(int argc, char** argv) {
    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&proc_num);
    MPI_Comm_size(MPI_COMM_WORLD,&comm_size);

    comm_size_cube_root = (int) cbrt(comm_size);

    if(!arg_check(argc,argv)) {
        if (proc_num == 0) {
            cout << "ERROR! Please enter valid arguments: " << endl;
            cout << "mpirun -np [COMM_SIZE] (OPTIONAL: --oversubscribe) ./main [N] [--print]" << endl;
            cout << "N: Grid Spacing (N>0)" << endl;
            cout << "N+1: Cube Size per Dimension" << endl;
            cout << "Assumption: (N+1) must be evenly divisible by the cube root of number of processors." << endl;
            cout << "--print: Enables printing the actual cube and calculated cube." << endl;
        }
        MPI_Finalize();
        return 0;
    }

    // Initialization of map-related variables.
    N = atoi(argv[1]);
    SIZE = N + 1;
    if(argc == 3)isPrint=true;

    // Initialization of communicator related variables.
    grid_size = SIZE / comm_size_cube_root;
    ghost_grid_size = grid_size + 2;

    // Initialization of Arrays!
    MPI_Datatype xy_plane;
    MPI_Datatype yz_plane;
    MPI_Datatype xz_plane;
    MPI_Type_vector(grid_size*grid_size,1,grid_size,MPI_DOUBLE,&xy_plane);
    MPI_Type_contiguous(grid_size*grid_size,MPI_DOUBLE,&yz_plane);
    MPI_Type_vector(grid_size,grid_size,grid_size*grid_size,MPI_DOUBLE,&xz_plane);
    MPI_Type_commit(&xy_plane);
    MPI_Type_commit(&yz_plane);
    MPI_Type_commit(&xz_plane);

    grid = new double[grid_size*grid_size*grid_size];
    ghost_grid = new double[(grid_size+2)*(grid_size+2)*(grid_size+2)];

    left_slice = new double[grid_size*grid_size];
    right_slice = new double[grid_size*grid_size];
    front_slice = new double[grid_size*grid_size];
    behind_slice = new double[grid_size*grid_size];
    top_slice = new double[grid_size*grid_size];
    down_slice = new double[grid_size*grid_size];


    // Processor related variables.
    x = get_proc_index(proc_num,'x');
    y = get_proc_index(proc_num,'y');
    z = get_proc_index(proc_num,'z');
    x_min = get_actual_boundary(proc_num,'x');
    x_max = x_min + grid_size;
    y_min = get_actual_boundary(proc_num,'y');
    y_max = y_min + grid_size;
    z_min = get_actual_boundary(proc_num,'z');
    z_max = z_min + grid_size;
    left_neighbor = get_neighbor(proc_num,'l');
    right_neighbor = get_neighbor(proc_num,'r');
    front_neighbor = get_neighbor(proc_num,'f');
    behind_neighbor = get_neighbor(proc_num,'b');
    top_neighbor = get_neighbor(proc_num,'t');
    down_neighbor = get_neighbor(proc_num,'d');

    initialize_grid();
    MPI_Barrier(MPI_COMM_WORLD);
    do{
        // send left & recv from right
        if(comm_size!=1){
            MPI_Request reqs_1[6];   // required variable for non-blocking calls
            MPI_Status stats_1[6];   // required variable for Waitall routine
            // SEND & RECV HERE!
            //Send yz-plane to left & right
            MPI_Issend((grid + 0*grid_size*grid_size + 0*grid_size + 0),1,yz_plane,left_neighbor,proc_num,MPI_COMM_WORLD,&reqs_1[0]);
            //Send xz-plane to front & behind
            MPI_Issend((grid + 0*grid_size*grid_size + 0*grid_size + 0),1,xz_plane,front_neighbor,proc_num,MPI_COMM_WORLD,&reqs_1[1]);
            //Send xy-plane to top & down
            MPI_Issend((grid + 0*grid_size*grid_size + 0*grid_size + 0),1,xy_plane,down_neighbor,proc_num,MPI_COMM_WORLD,&reqs_1[2]);

            //RECEIVE
            //Receive from left & right yz-planes
            MPI_Irecv(right_slice,grid_size*grid_size,MPI_DOUBLE,right_neighbor,right_neighbor,MPI_COMM_WORLD,&reqs_1[3]);
            //Receive from front & behind
            MPI_Irecv(behind_slice,grid_size*grid_size,MPI_DOUBLE,behind_neighbor,behind_neighbor,MPI_COMM_WORLD,&reqs_1[4]);
            //Receive from top & down
            MPI_Irecv(top_slice,grid_size*grid_size,MPI_DOUBLE,top_neighbor,top_neighbor,MPI_COMM_WORLD,&reqs_1[5]);
            MPI_Waitall(6, reqs_1, stats_1);

            MPI_Request reqs_2[6];   // required variable for non-blocking calls
            MPI_Status stats_2[6];   // required variable for Waitall routine
            MPI_Issend((grid + (grid_size-1)*grid_size*grid_size + 0*grid_size + 0),1,yz_plane,right_neighbor,proc_num,MPI_COMM_WORLD,&reqs_2[0]);
            MPI_Issend((grid + 0*grid_size*grid_size + (grid_size-1)*grid_size + 0),1,xz_plane,behind_neighbor,proc_num,MPI_COMM_WORLD,&reqs_2[1]);
            MPI_Issend((grid + 0*grid_size*grid_size + 0*grid_size + (grid_size-1)),1,xy_plane,top_neighbor,proc_num,MPI_COMM_WORLD,&reqs_2[2]);

            MPI_Irecv(left_slice,grid_size*grid_size,MPI_DOUBLE,left_neighbor,left_neighbor,MPI_COMM_WORLD,&reqs_2[3]);
            MPI_Irecv(front_slice,grid_size*grid_size,MPI_DOUBLE,front_neighbor,front_neighbor,MPI_COMM_WORLD,&reqs_2[4]);
            MPI_Irecv(down_slice,grid_size*grid_size,MPI_DOUBLE,down_neighbor,down_neighbor,MPI_COMM_WORLD,&reqs_2[5]);
            MPI_Waitall(6, reqs_2, stats_2);
        }
        // Form ghost grid.
        form_ghost_grid();

        // compute jacobi (consider boundaries ! )
        jacobi(grid,ghost_grid);

        //compute my_diff
        my_diff = compute_diff();
        // Synchronization
        MPI_Barrier(MPI_COMM_WORLD);
        //compute diff
        if(comm_size==1){
            diff = my_diff;
        }
        else{
            MPI_Allreduce(&my_diff,&diff,1,MPI_DOUBLE,MPI_SUM,MPI_COMM_WORLD);
        }
        if(proc_num == 0 && (iteration%10==0)){
            printf("Iteration=%d Error=%f\n",iteration,diff);
        }
        iteration++;
    } while(epsilon < diff);

    if(proc_num == 0){
        printf("Jacobi iterations ended.\n");
        printf("N=%d, Cube Size=%d, Iteration=%d, Error=%f\n",N,SIZE,iteration-1,diff);
    }
    /*
     * Error Calculations
     */
    actual_grid = new double[grid_size*grid_size*grid_size];
    initialize_actual_grid();
    double my_final_diff = compute_final_diff();
    double final_diff = 0.0;
    if(comm_size==1){
        final_diff = my_final_diff;
    }
    else{
        MPI_Allreduce(&my_final_diff,&final_diff,1,MPI_DOUBLE,MPI_SUM,MPI_COMM_WORLD);
    }
    if(proc_num == 0){
        printf("Error for Entire Cube=%f\n",final_diff);
    }
    /*
     * Printing actual and calculated cubes.
     */
    if(isPrint){
        if(comm_size==1){
            cout << endl;
            printf("Processor %d handles printing!\n",proc_num);
            printf("Printing the actual cube!\n");
            cout << endl;
            /*
             * Prints actual cube!
             */
            print_array(actual_grid,SIZE,SIZE,SIZE);
            /*
             * Prints calculated cube!
             */
            printf("Printing the calcualated cube!\n");
            cout << endl;
            print_array(grid,SIZE,SIZE,SIZE);
        }
        else{
            /*
             * Processor 0 collects the entire calculated cube!
             */
            MPI_Request reqs[comm_size-1];   // required variable for non-blocking calls
            MPI_Status stats[comm_size-1];
            if(proc_num!=0){
                MPI_Issend(grid,grid_size*grid_size*grid_size,MPI_DOUBLE,0,proc_num,MPI_COMM_WORLD,&reqs[proc_num-1]);
            }
            else{
                double* actual_cube = new double[SIZE*SIZE*SIZE];
                double* calculated_cube = new double[SIZE*SIZE*SIZE];
                double* grid_received = new double[grid_size*grid_size*grid_size];
                for(int index=1;index<comm_size;index++){
                    MPI_Irecv(grid_received,grid_size*grid_size*grid_size,MPI_DOUBLE,index,index,MPI_COMM_WORLD,&reqs[index-1]);
                    MPI_Wait(&reqs[index-1],&stats[index-1]);
                    int x_min_local = get_actual_boundary(index,'x');
                    int y_min_local = get_actual_boundary(index,'y');
                    int z_min_local = get_actual_boundary(index,'z');
                    for(int i=0;i<grid_size;i++){
                        for(int j=0;j<grid_size;j++){
                            for(int k=0;k<grid_size;k++){
                                *(calculated_cube + (i+x_min_local)*SIZE*SIZE + (j+y_min_local)*SIZE + (k+z_min_local)) = *(grid_received + i*grid_size*grid_size + j*grid_size + k);
                            }
                        }
                    }
                }
                // Processor 0 embeds its own grid into calculated cube!
                for(int i=0;i<grid_size;i++){
                    for(int j=0;j<grid_size;j++){
                        for(int k=0;k<grid_size;k++){
                            *(calculated_cube + (i)*SIZE*SIZE + (j)*SIZE + (k)) = *(grid + i*grid_size*grid_size + j*grid_size + k);
                        }
                    }
                }
                // Calculated cube is ready!
                /*
                 * Initializes the actual cube.
                 */
                initialize_actual_cube(actual_cube);
                cout << endl;
                printf("Processor %d handles printing!\n",proc_num);
                printf("Printing the actual cube!\n");
                cout << endl;
                /*
                 * Prints actual cube!
                 */
                print_array(actual_cube,SIZE,SIZE,SIZE);
                /*
                 * Prints calculated cube!
                 */
                printf("Printing the calcualated cube!\n");
                cout << endl;
                print_array(calculated_cube,SIZE,SIZE,SIZE);
                delete [] actual_cube;
                delete [] calculated_cube;
                delete [] grid_received;
            }
        }
    }
    deallocate_memory();
    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Finalize();
    return 0;
}

/*
 * HYPERPARAMETERS: Functions u and f.
 */

double u(double x,double y,double z){
    return x*y*z;
}

double f(double x,double y,double z) {
    return 0.0;
}

bool arg_check(int argc,char** argv){
    if(argc == 2 || argc == 3){
        int n = atoi(argv[1]);
        int size = n + 1;
        if(size <= 1 || mod(size,comm_size_cube_root) != 0)return false;
        if(argc == 3 && string(argv[2]) != "--print")return false;
        return true;
    }
    return false;
}

int mod(int number,int modulo){
    return (number % modulo < 0) ? number % modulo + modulo : number % modulo;
}

int get_actual_boundary(int proc_num, char dim){
    return get_proc_index(proc_num,dim) * grid_size;
}

int get_proc_index(int proc_num, char dim){
    switch (dim) {
        case 'x':
            return proc_num % comm_size_cube_root;
        case 'y':
            return (proc_num % (comm_size_cube_root * comm_size_cube_root)) / comm_size_cube_root;
        case 'z':
            return proc_num / (comm_size_cube_root * comm_size_cube_root);
        default:
            cout << "Error finding proc_index!" << endl;
            return -1;
    }
}

int get_proc_num(int x,int y,int z){
    return z * comm_size_cube_root * comm_size_cube_root + y * comm_size_cube_root + x;
}

int get_neighbor(int proc_num,char where){
    int x = get_proc_index(proc_num,'x');
    int y = get_proc_index(proc_num,'y');
    int z = get_proc_index(proc_num,'z');
    switch (where) {
        case 'l':
            return get_proc_num(mod(x-1,comm_size_cube_root),y,z);
        case 'r':
            return get_proc_num(mod(x+1,comm_size_cube_root),y,z);
        case 'f':
            return get_proc_num(x,mod(y-1,comm_size_cube_root),z);
        case 'b':
            return get_proc_num(x,mod(y+1,comm_size_cube_root),z);
        case 't':
            return get_proc_num(x,y,mod(z+1,comm_size_cube_root));
        case 'd':
            return get_proc_num(x,y,mod(z-1,comm_size_cube_root));
        default:
            cout << "Error finding neighbor!" << endl;
            return -1;
    }
}

bool is_boundary(int i,int j,int k){
    return ((i == 0 || i == SIZE-1) || (j == 0 || j == SIZE-1) || (k == 0 || k == SIZE-1));
}

void print_array(double *arr,int X,int Y,int Z){
    for(int i=0;i<X;i++){
        for(int j=0;j<Y;j++){
            for(int k=0;k<Z;k++){
                cout << *(arr + i*Y*Z + j*Z + k) << " ";
            }
            cout << endl;
        }
        cout << endl;
    }
}

void initialize_grid(){
    // For readability purposes...
    //printf("X: %d Y: %d Z: %d\n",grid_size,grid_size,grid_size);
    for(int i=0;i<grid_size;i++){
        for(int j=0;j<grid_size;j++){
            for(int k=0;k<grid_size;k++){
                int actual_i = x_min + i;
                int actual_j = y_min + j;
                int actual_k = z_min + k;
                *(grid + i*grid_size*grid_size + j*grid_size + k) = is_boundary(actual_i,actual_j,actual_k) ?  u(actual_i*1.0/(N),actual_j*1.0/(N),actual_k*1.0/(N)) : 0.0;
            }
        }
    }
}

void form_ghost_grid(){
    for(int i=0;i<grid_size;i++){
        for(int j=0;j<grid_size;j++){
            for(int k=0;k<grid_size;k++){
                *(ghost_grid + (i+1)*ghost_grid_size*ghost_grid_size + (j+1)*ghost_grid_size + (k+1)) = *(grid + i*grid_size*grid_size + j*grid_size + k);
            }
        }
    }
    // Left&right slices yz-plane
    for(int j=0;j<grid_size;j++){
        for(int k=0;k<grid_size;k++){
            *(ghost_grid + 0*ghost_grid_size*ghost_grid_size + (j+1)*ghost_grid_size + (k+1)) = *(left_slice + j*grid_size + k);
            *(ghost_grid + (ghost_grid_size-1)*ghost_grid_size*ghost_grid_size + (j+1)*ghost_grid_size + (k+1)) = *(right_slice + j*grid_size + k);
        }
    }
    // Front&behind slices xz-plane
    for(int i=0;i<grid_size;i++){
        for(int k=0;k<grid_size;k++){
            *(ghost_grid + (i+1)*ghost_grid_size*ghost_grid_size + 0*ghost_grid_size + (k+1)) = *(front_slice + i*grid_size + k);
            *(ghost_grid + (i+1)*ghost_grid_size*ghost_grid_size + (ghost_grid_size-1)*ghost_grid_size + (k+1)) = *(behind_slice + i*grid_size + k);
        }
    }// Top&down slices xy-plane
    for(int i=0;i<grid_size;i++){
        for(int j=0;j<grid_size;j++){
            *(ghost_grid + (i+1)*ghost_grid_size*ghost_grid_size + (j+1)*ghost_grid_size + (ghost_grid_size-1)) = *(top_slice + i*grid_size + j);
            *(ghost_grid + (i+1)*ghost_grid_size*ghost_grid_size + (j+1)*ghost_grid_size + 0) = *(down_slice + i*grid_size + j);
        }
    }
}

void jacobi(double *grid,double *ghost_grid){
    for(int i=1;i<grid_size+1;i++){
        for(int j=1;j<grid_size+1;j++){
            for(int k=1;k<grid_size+1;k++){
                int actual_i = x_min + (i-1);
                int actual_j = y_min + (j-1);
                int actual_k = z_min + (k-1);
                if(is_boundary(actual_i,actual_j,actual_k))continue;
                *(grid + (i-1)*grid_size*grid_size + (j-1)*grid_size + (k-1)) = 1.0/6 * (*(ghost_grid + (i-1)*ghost_grid_size*ghost_grid_size + j*ghost_grid_size + k) + *(ghost_grid + (i+1)*ghost_grid_size*ghost_grid_size + j*ghost_grid_size + k) +
                                                                  *(ghost_grid + i*ghost_grid_size*ghost_grid_size + (j-1)*ghost_grid_size + k) + *(ghost_grid + i*ghost_grid_size*ghost_grid_size + (j+1)*ghost_grid_size + k) +
                                                                  *(ghost_grid + i*ghost_grid_size*ghost_grid_size + j*ghost_grid_size + k - 1) + *(ghost_grid + i*ghost_grid_size*ghost_grid_size + j*ghost_grid_size + k + 1))
                                                         - (1.0/(6*(N)*(N)) * f(actual_i*1.0/(N),actual_j*1.0/(N),actual_k*1.0/(N)));
            }
        }
    }
}

double compute_diff(){
    double result = 0.0;
    for(int i=0;i<grid_size;i++){
        for(int j=0;j<grid_size;j++){
            for(int k=0;k<grid_size;k++){
                result += abs(*(grid + i*grid_size*grid_size + j*grid_size + k) - *(ghost_grid + (i+1)*(grid_size+2)*(grid_size+2) + (j+1)*(grid_size+2) + (k+1)));
            }
        }
    }
    return result;
}


void initialize_actual_grid(){
    for(int i=0;i<grid_size;i++){
        for(int j=0;j<grid_size;j++){
            for(int k=0;k<grid_size;k++){
                int actual_i = x_min + i;
                int actual_j = y_min + j;
                int actual_k = z_min + k;
                *(actual_grid + i*grid_size*grid_size + j*grid_size + k) = u(actual_i*1.0/(N),actual_j*1.0/(N),actual_k*1.0/(N));
            }
        }
    }
}

void initialize_actual_cube(double* cube){
    for(int i=0;i<SIZE;i++){
        for(int j=0;j<SIZE;j++){
            for(int k=0;k<SIZE;k++){
                *(cube + i*SIZE*SIZE + j*SIZE + k) = u(i*1.0/(N),j*1.0/(N),k*1.0/(N));
            }
        }
    }
}

double compute_final_diff(){
    double result = 0.0;
    for(int i=0;i<grid_size;i++){
        for(int j=0;j<grid_size;j++){
            for(int k=0;k<grid_size;k++){
                result += abs(*(grid + i*grid_size*grid_size + j*grid_size + k) - *(actual_grid + i*grid_size*grid_size + j*grid_size + k));
            }
        }
    }
    return result;
}

void deallocate_memory(){
    delete [] grid;
    delete [] ghost_grid;
    delete [] actual_grid;
    delete [] left_slice;
    delete [] right_slice;
    delete [] front_slice;
    delete [] behind_slice;
    delete [] top_slice;
    delete [] down_slice;
}
