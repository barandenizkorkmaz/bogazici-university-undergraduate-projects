#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <bits/stdc++.h>
#include <set>
using namespace std;

const int M=1000000007;
long long int powersOf29[1001];

long long int hashFunction(const char charArr[]){
    long long int hashValue=0;
    int size=strlen(charArr);
    for(int i=0;i<size;i++){
        hashValue+=((int)charArr[i]-96)*(powersOf29[i]%M);
        hashValue%=M;
    }
    return hashValue;
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        cout << "Run the code with the following command: ./project5 [input_file] [output_file]" << endl;
        return 1;
    }

    cout << "input file: " << argv[1] << endl;
    cout << "output file: " << argv[2] << endl;

    ifstream infile(argv[1]);
    set<long long int> set;
    string firstLine;
    infile >> firstLine;
    int sizeOfFirstLine=firstLine.size();
    long long int myArray[1100] = { 0 };
    myArray[0]=1;
    string line;
    int numOfWords;
    infile >> numOfWords;

    powersOf29[0]=1;
    for(int i=1;i<1001;i++){
        long long int before=powersOf29[i-1]%M;
        long long int newValue=before*29;
        newValue%=M;
        powersOf29[i]=newValue;
    }

    for(int i=0;i<numOfWords;i++){
        string word;
        infile >> word;
        int n=word.size();
        //cout << n;
        long long int hash=hashFunction(word.c_str());
        set.insert(hash);
    }

    for(int i=1;i<=sizeOfFirstLine;i++){
        for(int j=i;j<=sizeOfFirstLine;j++){
            string curWord = firstLine.substr(i-1, j-i+1);
            long long int currentWordHash=hashFunction(curWord.c_str());
            const bool is_in = set.find(currentWordHash) != set.end();
            if(is_in){
                myArray[j] += (myArray[i-1]%M);
                myArray[j] %= M;
            }
        }
    }

    long long int result=myArray[firstLine.size()];

    ofstream myFile;
    myFile.open(argv[2]);
    myFile << result;
    myFile.close();

    return 0;
}