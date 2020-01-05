//
// Created by bdk12 on 23.11.2018.
//

#ifndef PROJECT3_VERTEX_H
#define PROJECT3_VERTEX_H

#include <forward_list>
using namespace std;
class Vertex{
public:
    int value;
    int index;
    int lowLink;
    bool onStack;
    bool isVisited;
    bool isSource;
    forward_list<int> outEdges;
    forward_list<int> inEdges;
    Vertex();
    Vertex(int value);
    Vertex(const Vertex& v);
    Vertex& operator=(const Vertex& v);
    ~Vertex();
    bool operator=(const Vertex& v)const;



};
#endif //PROJECT3_VERTEX_H
