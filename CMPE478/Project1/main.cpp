/*
 * Author: Baran Deniz Korkmaz
 */

#include <iostream>
#include <stdlib.h>
#include <omp.h>
#include <vector>
#include <cmath>
#include <fstream>
#include <algorithm>
using namespace std;

bool argCheck(int argc, char* argv[]);
bool isNumeric(const string str);
bool fileExists(string& fileName);
bool writeCsvFile(string fileName, string col1, string col2, string col3, string col4, string col5, string col6, string col7, string col8, string col9, string col10);
void writeResults(int N,int MODE,int CHUNK_SIZE);
void calculate_primes_sequential(int M,int PRIMES[]);
vector<int> calculate_primes_parallel(int M,int PRIMES[], int SIZE_PRIMES,int MODE,int CHUNK_SIZE,int THREAD_NUMBER);
string getSchedulingMethod(int MODE);
void print_vector(vector<int> v);

vector<int> PRIMES_PARALLEL;
double SEQUENTIAL_TIME;
double PARALLEL_TIME;
int PRIMES_SEQUENTIAL=0;
int NUM_OF_PRIMES=0;
string FILE_NAME = "output.csv";
double TIME_RESULTS[3][4];
string SCHEDULING_METHOD;
bool printPrimes=false;
int THREAD_NUMBER=0;


int main(int argc, char* argv[]) {
    if(!argCheck(argc,argv)){
        cout << "Please enter valid arguments: [M (>=10)] [CHUNK_SIZE] (Optional: [--primes]) " << endl;
        return -1;
    }
    if(argc==4)printPrimes=true;
    int N = atoi(argv[1]);
    int CHUNK_SIZE = atoi(argv[2]);
    int SQRT_N = (int) (sqrt(N));
    int PRIMES[SQRT_N];

    for(int i=0;i<SQRT_N;i++){
        PRIMES[i] = 0;
    }
    int NUM_OF_THREADS[4] = {1,2,4,8};
    if(!fileExists(FILE_NAME)){
        writeCsvFile(FILE_NAME,"M","Scheduling Method","Chunk Size","T1","T2","T4","T8","S2","S4","S8");
    }

    SEQUENTIAL_TIME = omp_get_wtime();
    calculate_primes_sequential(SQRT_N,PRIMES);
    SEQUENTIAL_TIME = omp_get_wtime() - SEQUENTIAL_TIME;

    for(int MODE=0;MODE<=2;MODE++){
        for(int ITERATIONS=0;ITERATIONS<=3;ITERATIONS++){
            THREAD_NUMBER = NUM_OF_THREADS[ITERATIONS];
            SCHEDULING_METHOD = getSchedulingMethod(MODE);
            printf("Calculating %s mode with %d Threads:\n",SCHEDULING_METHOD.c_str(),THREAD_NUMBER);
            PARALLEL_TIME = omp_get_wtime();
            PRIMES_PARALLEL = calculate_primes_parallel(N,PRIMES,SQRT_N,MODE,CHUNK_SIZE,THREAD_NUMBER);
            NUM_OF_PRIMES = PRIMES_SEQUENTIAL + PRIMES_PARALLEL.size();
            printf("(%d,%d) Total Number of Primes: %d\n",MODE+1,ITERATIONS+1,NUM_OF_PRIMES);
            printf("(%d,%d) Total Duration: %f\n\n",MODE+1,ITERATIONS+1,SEQUENTIAL_TIME+PARALLEL_TIME);
            TIME_RESULTS[MODE][ITERATIONS] = SEQUENTIAL_TIME + PARALLEL_TIME;
        }
        writeResults(N,MODE,CHUNK_SIZE);
    }
    if(printPrimes){
        vector<int> RESULT;
        for(int i=0;i<PRIMES_SEQUENTIAL;i++)RESULT.push_back(PRIMES[i]);
        RESULT.insert(RESULT.end(),PRIMES_PARALLEL.begin(),PRIMES_PARALLEL.end());
        sort(RESULT.begin(),RESULT.end());
        printf("Printing the %d primes in the interval [2,%d]:\n",NUM_OF_PRIMES,N);
        print_vector(RESULT);
    }
    return 0;
}

bool argCheck(int argc, char* argv[]){
    if(argc!=3 && argc!=4)return false;
    if(argc==4 && string(argv[3]) != "--primes")return false;
    if(!isNumeric(argv[1]) || !isNumeric(argv[2]))return false;
    if(isNumeric(argv[1]) && atoi(argv[1])<10)return false;
    return true;
}

bool isNumeric(const string str)
{
    for(char x:  str)
        if(!isdigit(x))return false;

    return true;
}
/*
 * REFERENCE: https://raymii.org/s/snippets/Cpp_create_and_write_to_a_csv_file.html
 */
bool fileExists(string& fileName){
    return static_cast<bool>(ifstream(fileName));
}

void writeResults(int N,int MODE,int CHUNK_SIZE){
    string SCHEDULING_METHOD;
    switch (MODE){
        case 0:
            SCHEDULING_METHOD="Static";
            break;
        case 1:
            SCHEDULING_METHOD="Dynamic";
            break;
        case 2:
            SCHEDULING_METHOD="Guided";
            break;
    }
    double T_1 = TIME_RESULTS[MODE][0];
    double T_2 = TIME_RESULTS[MODE][1];
    double T_4 = TIME_RESULTS[MODE][2];
    double T_8 = TIME_RESULTS[MODE][3];
    double S_2 = T_1 / T_2;
    double S_4 = T_1 / T_4;
    double S_8 = T_1 / T_8;
    writeCsvFile(FILE_NAME, to_string(N), SCHEDULING_METHOD, to_string(CHUNK_SIZE), to_string(T_1), to_string(T_2), to_string(T_4), to_string(T_8), to_string(S_2), to_string(S_4), to_string(S_8));
}

bool writeCsvFile(string fileName, string col1, string col2, string col3, string col4, string col5, string col6, string col7, string col8, string col9, string col10) {
    fstream outFile;
    outFile.open(fileName,ios::out|ios::app);
    if(outFile){
        outFile << col1 << "," << col2 << "," << col3 << "," << col4 << "," << col5 << "," << col6 << "," << col7 << "," << col8 << "," << col9 << "," << col10 << "\n";
        outFile.close();
        return true;
    }
    return false;
}

string getSchedulingMethod(int MODE){
    switch(MODE){
        case 0:
            return "Static";
        case 1:
            return "Dynamic";
        case 2:
            return "Guided";
    }
}

void calculate_primes_sequential(int M, int PRIMES[]){
    int K,J,QUO,REM,n;
    PRIMES[0]=2;
    PRIMES[1]=3;
    PRIMES_SEQUENTIAL+=2;
    J=1;

    for(n=5;n<=M;n+=2){
        K=1;
        while(1){
            QUO=n/PRIMES[K];
            REM=n%PRIMES[K];
            if(REM==0){
                break;
            }
            else if(QUO<=PRIMES[K] || PRIMES[K+1]==0){
                J+=1;
                PRIMES[J]=n;
                PRIMES_SEQUENTIAL++;
                break;
            }
            else{
                K+=1;
            }
        }
    }

}

vector<int> calculate_primes_parallel(int M, int PRIMES[], int SIZE_PRIMES, int MODE, int CHUNK_SIZE, int THREAD_NUMBER){
    vector<int> result_vector;
    int K,J,QUO,REM, n;
    n=M;
    int START_INDEX = (SIZE_PRIMES%2 == 1) ? (SIZE_PRIMES+2) : SIZE_PRIMES+1;

    switch(MODE){
        case 0:
            omp_set_schedule(omp_sched_static,CHUNK_SIZE);
            break;
        case 1:
            omp_set_schedule(omp_sched_dynamic,CHUNK_SIZE);
            break;
        case 2:
            omp_set_schedule(omp_sched_guided,CHUNK_SIZE);
            break;
    }

    omp_set_num_threads(THREAD_NUMBER);

    #pragma omp parallel shared(n,result_vector,PRIMES,START_INDEX) private(K,J,QUO,REM)
    {
        vector<int> vec_private;
        #pragma omp for schedule(runtime) nowait
        for (J = START_INDEX; J <= n; J += 2) {
            K = 1;
            while (1) {
                QUO = J / PRIMES[K];
                REM = J % PRIMES[K];
                if (REM == 0) {
                    break;
                } else if (QUO <= PRIMES[K] || PRIMES[K+1] == 0) {
                    vec_private.push_back(J);
                    break;
                } else {
                    K += 1;
                }
            }
        }
        // It's time to measure parallel computation duration.
        #pragma omp master
            if(1){
                PARALLEL_TIME = omp_get_wtime() - PARALLEL_TIME;
            }
        #pragma omp critical
            if (1) {
                result_vector.insert(result_vector.end(), vec_private.begin(), vec_private.end());
            }
    }
    return result_vector;
}

void print_vector(vector<int> v){
    for(int & it : v){
        cout << it << " ";
    }
    cout << endl;
}
