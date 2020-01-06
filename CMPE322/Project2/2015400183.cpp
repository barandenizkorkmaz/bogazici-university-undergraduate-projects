/*
 * Author: Baran Deniz Korkmaz
 * Student ID: 2015400183
 */

#include <iostream>
#include <pthread.h>
#include <fstream>
#include <unistd.h>
#include <sstream>
#include <time.h>
#include <vector>

using namespace std;

//Define constants that will be used.
#define NUMATM 10
#define NUMOPS 5
#define NANO_SECOND_MULTIPLIER  1000000

/*
 * The data structure for the customers.
 * The data for the customers include customer id, sleep duration of customer,
 * id of atm that the customer will use, type of payment that customer will make, and payment amount.
 */

struct customer_data{
    int customer_id;
    int sleep_duration;
    int atm;
    int payment_type;
    int payment_amt;
    string payment_type_str;
};

/*
 * The data structure for the ATMs.
 * The data for the ATMs include atm id, and the number of customers expected in the system in overall.
 */
struct atm_data{
    int atm_id;
    int num_of_customers;
};

//Define global variables that will be shared between threads.
/*
 * Let us briefly explain the functionalities of the variables:
 * 1. out_file: The output file that will be written.
 * 2. mtx_main_atm: This mutex is locked whenever a customer begins its operations in an atm.
 * 3. mtx_atm_wait: This mutex is locked in order to enable that the customer will wait until the operations that the customer requested are provided by the atm thread.
 * 4. mtx_done_atm: This conditional mutex is used together with mtx_atm_wait to enable conditional execution.
 * 5. mtx_ops: This mutex is locked in order to enable that payment operations of the same type bill will not be carried out simultaneously.
 * 6. mtx_counter: This mutex is locked when a thread wants to increase the variable counter.
 * 7. mtx_file: This mutex is locked when an atm thread wants to write into the output file.
 * 8. is_done: This array can be considered as a boolean array which is used to inform whether the atm has finished its operation while the customer is waiting for it to finish.
 * 9. is_waiting_client: This array can be considered as a boolean array which is used to inform an atm thread that a new customer is now ready to use atm.
 * 10. payments: This array contains the total amounts of payments for a specific type of payment.
 * 11. counter: This varible holds the number of customers that finished their operations and left the queue.
 * 12. atm_client_array: This array holds the data of the customer that will use the atm with id i (i is equivalent to the array index + 1 ) i.e atm with id 1 is checks the first index (index of 0) of array.
 */
ofstream out_file;
pthread_mutex_t mtx_main_atm[NUMATM];
pthread_mutex_t mtx_atm_wait[NUMATM];
pthread_cond_t mtx_done_atm[NUMATM];
pthread_mutex_t mtx_ops[NUMOPS];
pthread_t atm_thread[NUMATM];
pthread_mutex_t mtx_counter;
pthread_mutex_t mtx_file;
int is_done[10]={0,0,0,0,0,0,0,0,0,0};
int is_waiting_client[10]={0,0,0,0,0,0,0,0,0,0};
int payments[5]={0,0,0,0,0};
int counter=0;
customer_data atm_client_array[NUMATM];

/*
 * The customer threads executes the customer_thread_function function.
 */
void *customer_thread_function(void *customer_args){
    struct customer_data *my_data;
    my_data = (struct customer_data *) customer_args;
    int sleep_duration=my_data->sleep_duration;

    //The customer sleeps for a specific time duration in miliseconds.
    //Reference: https://stackoverflow.com/questions/7684359/how-to-use-nanosleep-in-c-what-are-tim-tv-sec-and-tim-tv-nsec
    timespec sleepValue = {0};
    sleepValue.tv_nsec = sleep_duration*NANO_SECOND_MULTIPLIER;
    nanosleep(&sleepValue, NULL);

    //The customer locks the atm that it will use.
    int atm_num=my_data->atm;
    pthread_mutex_lock(&mtx_main_atm[atm_num-1]);
    pthread_mutex_lock(&mtx_atm_wait[atm_num-1]);
    //overwrite the array for this atm.
    int customer_id=my_data->customer_id;
    int payment_type=my_data->payment_type;
    int payment_amt=my_data->payment_amt;
    string payment_type_str=my_data->payment_type_str;
    atm_client_array[atm_num-1].customer_id=customer_id;
    atm_client_array[atm_num-1].atm=atm_num;
    atm_client_array[atm_num-1].payment_type=payment_type;
    atm_client_array[atm_num-1].payment_amt=payment_amt;
    atm_client_array[atm_num-1].payment_type_str=payment_type_str;
    //Customer indicates that it is waiting for the atm with id of atm_num.
    is_waiting_client[atm_num-1]=1;

    //The customer waits until the atm executes its operations.
    if(!is_done[atm_num-1]){
        pthread_cond_wait(&mtx_done_atm[my_data->atm-1],&mtx_atm_wait[atm_num-1]);
    }
    //The is_done value of the atm is reset for proper future use of other customers.
    is_done[atm_num-1]=0;

    //The customer locks mtx_counter to change the value of counter variable.
    pthread_mutex_lock(&mtx_counter);
    counter++;
    pthread_mutex_unlock(&mtx_counter);

    //The customer unlocks the locks of the atm that it has operated.
    pthread_mutex_unlock(&mtx_atm_wait[atm_num-1]);
    pthread_mutex_unlock(&mtx_main_atm[atm_num-1]);

    pthread_exit(NULL);
}

/*
 * The atm threads executes the atm_thread_function function.
 */
void *atm_thread_function(void *atm_args){
    struct atm_data *my_data;
    my_data = (struct atm_data *) atm_args;
    int atm_num=my_data->atm_id;
    int num_of_customers=my_data->num_of_customers;
    //The atms keep operating until all of the customers leave the system.
    while(counter<num_of_customers){
        if(is_waiting_client[atm_num-1]){//If a customer is waiting for its operations, the atm begins to execute.
            //The atm locks the mutex that is unlocked by the conditional wait signaled by the customer that wants to operate on the atm.
            pthread_mutex_lock(&mtx_atm_wait[atm_num-1]);
            int payment_type=atm_client_array[atm_num-1].payment_type;
            //The atm locks the mutex of payment that it will carry out in order to prevent simultaneous execution of same type of payment with other atms.
            pthread_mutex_lock(&mtx_ops[payment_type]);
            int payment_amt=atm_client_array[atm_num-1].payment_amt;
            //Payment is transacted into the bill account.
            payments[payment_type]+=payment_amt;
            //As the payment is done, the atm locks the mtx_file and writes the output of the payment information into the file.
            pthread_mutex_lock(&mtx_file);
            string payment_type_str=atm_client_array[atm_num-1].payment_type_str;
            out_file << "Customer" << atm_client_array[atm_num-1].customer_id << "," << payment_amt << "TL," << payment_type_str << endl;
            pthread_mutex_unlock(&mtx_file);
            pthread_mutex_unlock(&mtx_ops[payment_type]);
            //The atm indicates that it has carried out its operations and has no waiting customer at the moment.
            is_waiting_client[atm_num-1]=0;
            is_done[atm_num-1]=1;
            pthread_cond_signal(&mtx_done_atm[atm_num-1]);
            pthread_mutex_unlock(&mtx_atm_wait[atm_num-1]);
        }
    }
    pthread_exit(NULL);
}

int main(int argc, char **argv) {
    string line;
    //The variable of input file that will enable reading the input.
    fstream in_file;
    string infile=argv[1];
    in_file.open(infile);
    //Split the name of the input file by dot as delimiter.
    istringstream iss(infile);
    vector<string> tokens;
    string token;
    while (std::getline(iss, token, '.')) {
        if (!token.empty())
            tokens.push_back(token);
    }
    //The name of the output file is the substring of the name of input file until a dot is encountered.
    string out_file_name=tokens[0]+"_log.txt";
    out_file.open(out_file_name);
    //Read the first line of the input file to set the number of customers.
    in_file>>line;
    int num_of_customers;
    num_of_customers=stoi(line);
    //Initialize customer threads.
    pthread_t customer_thread[num_of_customers];
    customer_data customer_data_array[num_of_customers];
    atm_data atm_data_array[NUMATM];
    //Initialize the mutexes.
    for (int i = 0; i < NUMATM; i++){
        pthread_mutex_init(&mtx_main_atm[i], NULL);
        pthread_mutex_init(&mtx_atm_wait[i],NULL);
    }
    for (int i = 0; i < NUMOPS; i++){
        pthread_mutex_init(&mtx_ops[i], NULL);
        pthread_cond_init(&mtx_done_atm[i],NULL);
    }
    pthread_mutex_init(&mtx_counter,NULL);
    pthread_mutex_init(&mtx_file,NULL);
    //For each customer, we read the input and create the data that will be passed into its own thread.
    for (int i = 1 ; i <= num_of_customers ; ++i){
        in_file>>line;
        stringstream ss (line);
        string item;
        int temp_arr[4];
        int current_element;
        int elem_num=0;
        struct customer_data customer_data;
        while (getline (ss, item, ',')) {
            if(elem_num==2){
                if(item=="cableTV"){
                    current_element=0;
                }
                else if(item=="electricity"){
                    current_element=1;
                }
                else if(item=="gas"){
                    current_element=2;
                }
                else if(item=="telecommunication"){
                    current_element=3;
                }
                else if(item=="water"){
                    current_element=4;
                }
                else{//Illegal Input
                    cout << "Illegal Input" << endl;
                    return -1;
                }
                customer_data.payment_type_str=item;
            }
            else {
                current_element = stoi(item);
            }
            temp_arr[elem_num]=current_element;
            elem_num++;
        }
        customer_data.customer_id=i;
        customer_data.sleep_duration=temp_arr[0];
        customer_data.atm=temp_arr[1];
        customer_data.payment_type=temp_arr[2];
        customer_data.payment_amt=temp_arr[3];
        customer_data_array[i-1]=customer_data;
    }
    //Creation of atm threads and the pass of their data has been carried out.
    for(int i=0;i<NUMATM;i++){
        struct atm_data atm_data;
        atm_data.atm_id=i+1;
        atm_data.num_of_customers=num_of_customers;
        atm_data_array[i]=atm_data;
        int t = pthread_create(&atm_thread[i], NULL, &atm_thread_function, (void*) &atm_data_array[i]);//index is set 1 by default
        if (t != 0)cout << "Error in thread creation: " << t << endl;
    }
    //Creation of customer threads and the pass of their data has been carried out.
    for(int i=0;i<num_of_customers;i++){
        int t = pthread_create(&customer_thread[i], NULL, &customer_thread_function, (void*) &customer_data_array[i]);//index is set 1 by default
        if (t != 0)cout << "Error in thread creation: " << t << endl;
    }
    //The main thread waits for customer and atm threads to finish their executions.
    for(int i=0;i<num_of_customers;i++){
        pthread_join(customer_thread[i],NULL);
    }
    for(int i=0;i<NUMATM;i++){
        pthread_join(atm_thread[i],NULL);
    }
    //Main thread writes the final status of payments into the output file.
    out_file << "All payments are completed." << endl;
    out_file << "CableTV: " << payments[0] << "TL" << endl;
    out_file << "Electricity: " << payments[1] << "TL" << endl;
    out_file << "Gas: " << payments[2] << "TL" << endl;
    out_file << "Telecommunication: " << payments[3] << "TL" << endl;
    out_file << "Water: " << payments[4] << "TL" << endl;

    in_file.close();
    out_file.close();
    return 0;
}

