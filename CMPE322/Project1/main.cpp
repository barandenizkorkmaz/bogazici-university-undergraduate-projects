/*
 * Author: Baran Deniz Korkmaz
 * Student ID: 2015400183
 *
 */

#include <iostream>
#include <vector>
#include <string>
#include <stdio.h>
#include<dirent.h>
#include <sstream>
#include <fstream>
#include <algorithm>
#include <sys/wait.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

using namespace std;
void addHistory(vector<string> &v,string s);
void printHistory(vector<string> &v);
string getCommand(vector<string> &v);
void exec(char** command);
void execp(char** command1,char** command2);
void execr(char** command,char* file);

//Counts the number of commands prompted by the user.
static int counter=0;


int main(int argc, char* argv[]) {
    vector<string> history; //Vector of strings which holds the commands prompted by the user.
    while(1){
        string input;
        cout << getenv("USER") << " >>> "; //Provides a shell interface by printing 'username >>>' in the beginning of each line.
        getline(std::cin, input); //Reads the input.
        if(!(input.find_first_not_of(' ') != std::string::npos)) //Checks if the input contains any characters except spaces.
        {
            continue;
        }
        addHistory(history,input); //Add the input into the history vector which records the entry history.
        counter++;
        vector<string> commandVector;
        istringstream iss(input);
        for(string s; iss >> s; ) //Each index of commandVector contains the parsed string which is seperated by space(s).
            commandVector.push_back(s);
        string command = *(commandVector.begin());
        string commandLineInput=getCommand(commandVector);//The user input as a string whereby each word is seperated by a single space.
        if(command == "listdir"){ //Implementation of the commands starts by listdir which contains listdir, listdir -a, listdir | grep "args", listdir -a | grep "args".
            if(commandLineInput=="listdir"){ //Executes the ls command which is the case when the input is "listdir".
                char* cmd[]={(char*)"ls",NULL};//The array of char pointers which holds the pointers to the arguments of the command to be executed. The array ends with an element of NULL which provides the correct execution of execvp command.
                exec(cmd);
            }
            else if(commandLineInput=="listdir -a"){//Executes the ls -a command which is the case when the input is "listdir -a".
                char* cmd[]={(char*)"ls",(char*)"-a",NULL};
                exec(cmd);
            }
            else if(commandVector[1]=="|" && commandVector[2]=="grep" && commandVector.size()>3){//Executes the ls | grep "arg" command which is the case when the input is "listdir | grep "arg".
                string arg=input.substr(input.find_first_of('"')+1);
                arg=arg.substr(0,arg.size()-1); //The argument is the string between the first and the last quotation marks.
                //cout << arg << endl;
                char* cmd1[]={(char*)"ls",NULL};//The array of char pointers which holds the pointers to the arguments of the command to be executed. The array ends with an element of NULL which provides the correct execution of execvp command.
                char* cmd2[]={(char*)"grep",(char*)arg.c_str(),NULL};
                execp(cmd1,cmd2);
            }
            else if(commandVector[1]=="-a" && commandVector[2]=="|" && commandVector[3]=="grep" && commandVector.size()>4){//Executes the ls -a | grep "arg" command which is the case when the input is "listdir -a | grep "arg".
                string arg=input.substr(input.find_first_of('"')+1);
                arg=arg.substr(0,arg.size()-1); //The argument is the string between the first and the last quotation marks.
                //cout << arg << endl;
                char* cmd1[]={(char*)"ls",(char*)"-a",NULL};
                char* cmd2[]={(char*)"grep",(char*)arg.c_str(),NULL};
                execp(cmd1,cmd2);
            }
            else{//The case where the input given is not valid for any of listdir commands.
                cout << commandLineInput + ": command not found" << endl;
            }
        }
        else if(command == "currentpath" && commandVector.size()==1){//Executes the pwd command which is the case when the input is "currentpath".
            char* cmd[]={(char*)"pwd",NULL};
            exec(cmd);
        }
        else if(command == "printfile"){//Implementation of the commands starts by printfile which contains printfile arg, printfile arg1 > arg2.
            if(commandVector.size()==2){//Executes the cat command which is the case when the input is "prinfile fileName".
                string fileName=commandVector[1];
                char* cmd[]={(char*)"cat",(char*)fileName.c_str(),NULL};
                exec(cmd);
            }
            else if(commandVector.size()==4 && commandVector[2]==">"){//Executes the cat fileName1 > fileName2 command which is the case when the input is "printfile fileName1 > fileName2".
                string inFile=commandVector[1];
                string outFile=commandVector[3];
                char* cmd[]={(char*)"cat",(char*)inFile.c_str(),NULL};
                execr(cmd,(char*)outFile.c_str());
            }
            else{//The case where the input given is not valid for any of printfile commands.
                cout << commandLineInput + ": command not found" << endl;
            }
        }
        else if(command == "footprint" && commandVector.size()==1){//Executes the history command which is the case when the input is "footprint".
            printHistory(history);
        }
        else if(command == "exit" && commandVector.size()==1){//The terminal exits.
            break;
        }
        else{//The case where the input given is not valid for any operations.
            cout << commandLineInput + ": command not found" << endl;
        }
    }
    return 0;
}

void addHistory(vector<string> &v,string s) {//Adds the given input into the history vector.
    if(v.size()==15){
        v.erase(v.begin());
    }
    v.push_back(s);
}

void printHistory(vector<string> &v){//Prints the history when the given input is "footprint"
    int index=1;
    if(counter>15){
        index=counter-15+1;
    }
    for(vector<string>::iterator it =v.begin();it!=v.end();it++){
        cout << index << " " << *it << endl;
        index++;
    }
}

string getCommand(vector<string> &v){//Enables decoding the given input in a way such that the input has been brought into a form that it contains each word seperated by a space.
    string s="";
    vector<string>::iterator it =v.begin();
    for(;it!=v.end()-1;it++){
        s+=*it+" ";
    }
    s+=*it;
    return s;
}

void exec(char** command){//Executes the commands that requires no redirection or pipe.
    pid_t pid;
    pid=fork(); //Forking a child.
    if(pid==-1){//If the fork fails, the return value will be -1.
        perror("fork failed");
    }
    if(pid==0){ //Child process executes.
        execvp(command[0],command);
    }
    else{ //Parent waits child to execute and terminate. In our case, the parent is the main code that is implementing the terminal via a while loop which always iterates unless it's terminated.
        waitpid(pid,NULL,0);
    }
}

void execp(char** command1,char** command2){//Executes the commands that requires a single pipe.
    int fd[2];
    pipe(fd);

    pid_t pid1=fork();//The pid1 is initialized to hold the return value for the forking of the first child which will execute the first command of the pipe..
    pid_t pid2;//The pid2 is initialized to hold the return value for the forking of the second child which will execute the second command of the pipe.
    if(pid1==-1){//Fork failed.
        perror("fork failed");
    }
    if(pid1==0) //First child process executes that is the first command of the pipe.
    {
        dup2(fd[1], 1); //Redirects the stdout of the first execution into the second index of the file descriptor.
        close(fd[0]); //Close the first index of the file descriptor since we will not use it.
        execvp(command1[0], command1); //The first command of the pipe executes.
        fprintf(stderr, "Failed to execute '%s'\n", "ls");
        //exit(1);
    }
    else
    {
        if(pid2=fork()==0) //Second child process executes that is the second command of the pipe.
        {
            dup2(fd[0], 0); //The stdin of the second execution will be redirected from the input part of the pipe.
            close(fd[1]); //Close the unused unput of the file descriptor since it will not be used.
            execvp(command2[0], command2); //The second command of the pipe executes.
            fprintf(stderr, "Failed to execute '%s'\n", "grep");
            //exit(1);
        }
    }
    waitpid(pid1,NULL,0); //Parent waits for the first child to terminate.
    close(fd[1]);
    waitpid(pid2,NULL,0); //Parent waits for the second child to terminate.
    close(fd[0]);
}


/*
 * Credits for the following method: https://stackoverflow.com/questions/2605130/redirecting-exec-output-to-a-buffer-or-file?fbclid=IwAR0Ad00Ibqp3-yWFmfp3ivLjRqO_D5ObI_RYENFT7q6sg0pS5oA8PMz80Y0
 */
void execr(char** command,char* file){ //Executes the commands that requires redirection which is the case where the input is "printfile fileName1 > fileName2".
    pid_t pid1;
    if ((pid1=fork()) == 0)
    {
        //Child process executes.
        int fd = open(file, O_RDWR | O_CREAT, S_IRUSR | S_IWUSR);

        dup2(fd, 1); //Makes stdout to be written into the file.

        close(fd); //Fd is no longer needed.

        execvp(command[0],command); //Executes the given command.
    }
    else{
        waitpid(pid1,NULL,0); //Parent waits for the child to terminate.
    }

}
