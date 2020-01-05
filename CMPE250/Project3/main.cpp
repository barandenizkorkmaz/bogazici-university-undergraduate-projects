#include <iostream>
#include <fstream>
#include <sstream>
#include <iterator>
#include <time.h>
#include <vector>
#include <string>
#include <forward_list>

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
    //clock_t tStart = clock();
    // below reads the input file
    // in your next projects, you will implement that part as well

    if (argc != 3) {
        cout << "Run the code with the following command: ./project2 [input_file] [output_file]" << endl;
        return 1;
    }

    cout << "input file: " << argv[1] << endl;
    cout << "output file: " << argv[2] << endl;

    // here, perform the input operation. in other words,
    // read the file named <argv[1]>

    //ifstream infile(argv[1]);
    //file.open("C:\\Users\\bdk12\\Desktop\\input1.txt", ios::in);
    ifstream infile(argv[1]);
    string line;
    getline(infile,line); //firstLine
    int numOfVertices=stoi(line);
    Graph g(numOfVertices);
    for(int i=1;i<=numOfVertices;i++){
        getline(infile,line);
        vector<string> words;
        split1(line,words);
        int numOfChildren=stoi(words[0]);
        for(int j=1;j<=numOfChildren;j++){
            int index=stoi(words[j]);
            if(i!=index) {
                g.vertices[i - 1].outEdges.push_front(g.vertices[index - 1].value);
                g.vertices[index - 1].inEdges.push_front(g.vertices[i - 1].value);
            }
        }
    }

    //cout << "input file has been read" << endl;

    // here, perform the output operation. in other words,
    // print your results into the file named <argv[2]>
    // print the avg waiting time and # of passengers missing their flight
    ofstream myFile;
    myFile.open (argv[2]);

    //ofstream outfile ("C:\\Users\\bdk12\\Desktop\\output1.txt");

    g.scc();
    g.findCracks();
    myFile << g.cracks.size() << " ";
    for(vector<Vertex>:: iterator itr=g.cracks.begin();itr!=g.cracks.end();itr++){
        myFile << (*itr).value << " ";
    }

    //outfile.close();
    myFile.close();
    //printf("Time taken: %.10fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);
    return 0;
}