#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <iterator>
#include "SurveyClass.h"
#include "LinkedList.h"
using namespace std;

template <class Container>
void split1(const string& str, Container& cont)
{
    istringstream iss(str);
    copy(istream_iterator<string>(iss),
              istream_iterator<string>(),
              back_inserter(cont));
}

float findAmount(const vector<string> words)
{
    float return_value = 0;
    for(int i=0; i<words.size(); i++){
        if (words[i][0] == '$') {
            const char *cstr = (words[i].substr(1)).c_str();
            return_value = strtof(cstr, NULL);
            cout << "return_value: " << return_value << endl;
            break;
        }
    }
    return return_value;
}

int main(int argc, char* argv[]) {
    // below reads the input file
    // in your next projects, you will implement that part as well
    /*
    if (argc != 3) {
        cout << "Run the code with the following command: ./project1 [input_file] [output_file]" << endl;
        return 1;
    }

    cout << "input file: " << argv[1] << endl;
    cout << "output file: " << argv[2] << endl;



    // here, perform the input operation. in other words,
    // read the file named <argv[1]>
    ifstream infile(argv[1]);
    string line;
    vector<string> input;
    // process first line
    getline(infile, line);
    int N = stoi(line);
    cout << "number of input lines: " << N << endl;

    SurveyClass mySurveyClass;
    for (int i=0; i<N; i++) {
        getline(infile, line);
        cout << "line: " << line << endl;

        vector<string> words;
        split1(line,words);
        string curr_name = words[0];
        float curr_amount = findAmount(words);

        mySurveyClass.handleNewRecord(curr_name, curr_amount);
    }

    cout << "input file has been read" << endl;

    float minExp = mySurveyClass.calculateMinimumExpense();
    float maxExp = mySurveyClass.calculateMaximumExpense();
    float avgExp = mySurveyClass.calculateAverageExpense();

    // here, perform the output operation. in other words,
    // print your results into the file named <argv[2]>
    ofstream myfile;
    myfile.open (argv[2]);
    myfile << minExp << " " << maxExp << " " << avgExp << endl;
    myfile.close();

    cout << "minExp " << minExp << endl;
    cout << "maxExp " << maxExp << endl;
    cout << "avgExp " << avgExp << endl;
    */

    SurveyClass sur1;
    sur1.handleNewRecord("deniz",20);
    sur1.members->pushTail("affan",40);
    sur1.members->updateNode("deniz",12);
    sur1.handleNewRecord("affan",24);
    sur1.members->print();
    SurveyClass sur2;
    sur2=move(sur1);
    sur2.members->print();
    sur2.handleNewRecord("dilan",36);
    sur2.handleNewRecord("affan", 0);
    sur2.members->print();
    sur2.members->updateNode("affan",24);
    sur2.members->pushTail("doğu",48);
    sur2.members->print();
    sur2.members->~LinkedList();
    sur2.members->print();

    /*
    LinkedList list1;
    list1.pushTail("deniz",12);
    list1.pushTail("dilan",24);
    list1.print();
    LinkedList list2;
    list2=move(list1);
    list2.print();
    list2.pushTail("ceylan",36);
    list1.print();
    list2.print();
    */

    /*
    float var=20.256;
    cout << var*100 << endl;
    int s=var*100;
    cout << s << endl;
    float result=s;
    result=result/100;
    cout << result << endl;

    */
    /*
    SurveyClass sur2=move(sur1);
    sur1.handleNewRecord("deniz",30);
    sur2.members->updateNode("deniz",50);
    sur2.members->pushTail("doğu",100);
    sur1.members->print();
    sur2.members->print();
    */
   // sur1.~SurveyClass();
    //sur1.members->print();
    //LinkedList list1;
    //list1.pushTail("deniz",11500);
    //list1.pushTail("dilan",6000);
    //LinkedList list2;
    //list2=move(list1);
    //list2=move(list1);
    //list1.print();
    //list2.print();

    //list.pushTail("deniz",20);
    //list.pushTail("doğu",100);
    //list.print();
    //LinkedList list2(list);
    //list2.print();
    //LinkedList list3;
    //list3=list2;
    //list3.updateNode("deniz",30);
    //list2.print();
    //list3.print();
    //list.updateNode("deniz",30);
    //list2.updateNode("doğu",40);
    //list.print();
    //list2.print();
    //list.~LinkedList();
    //list.print();
    //list2.print();


    //list.pushTail("dilan",60);
    //list.pushTail("beko",80);
    //list.print();
    //list.updateNode("beko",40);



    return 0;
}
