#include <iostream>
#include <fstream>
#include <sstream>

#include <iterator>
#include <vector>
#include <string>
#include <array>
#include <queue>

#include <time.h>
#include "Graph.h"
#include "Vertex.h"

using namespace std;

template <class Container>
void split1(const string& str, Container& cont)
{
    istringstream iss(str);
    copy(istream_iterator<string>(iss), istream_iterator<string>(), back_inserter(cont));
}

int main(int argc, char* argv[]) {
    // below reads the input file
    // in your next projects, you will implement that part as well

    if (argc != 3) {
        cout << "Run the code with the following command: ./project4 [input_file] [output_file]" << endl;
        return 1;
    }

    cout << "input file: " << argv[1] << endl;
    cout << "output file: " << argv[2] << endl;

    // here, perform the input operation. in other words,
    // read the file named <argv[1]>

    ifstream infile(argv[1]);
    string line;
    getline(infile,line);
    vector<string> words;
    split1(line,words);
    int row=stoi(words[0]);
    int col=stoi(words[1]);
    Graph g(row,col);
    for(int i=0;i<row;i++){
        getline(infile,line);
        vector<string> words;
        split1(line,words);
        for(int j=0;j<col;j++){
            int currentHeight=stoi(words[j]);
            (*(g.map+i)+j)->x=i;
            (*(g.map+i)+j)->y=j;
            (*(g.map+i)+j)->height=currentHeight;
            (*(g.map+i)+j)->heightDifference=0;
        }
    }

    for(int i=0;i<row;i++){
        for(int j=0;j<col;j++){
            if(j!=0){
                g.map[i][j].neighbors.push_back(make_pair(i,j-1));
            }

            if(j!=col-1){
                g.map[i][j].neighbors.push_back(make_pair(i,j+1));
            }

            if(i!=0){
                g.map[i][j].neighbors.push_back(make_pair(i-1,j));
            }

            if(i!=row-1){
                g.map[i][j].neighbors.push_back(make_pair(i+1,j));
            }
        }
    }

    cout << "input file has been read" << endl;

    // here, perform the output operation. in other words,
    // print your results into the file named <argv[2]>

    ofstream myFile;
    myFile.open (argv[2]);

    getline(infile,line);
    getline(infile,line);
    vector<string> words2;
    split1(line,words2);
    int x1=stoi(words2[0]);
    int y1=stoi(words2[1]);
    int x2=stoi(words2[2]);
    int y2=stoi(words2[3]);

    g.findHeight(x1,y1,x2,y2);
    myFile << g.maxHeight << endl;
    myFile.close();

    return 0;
}