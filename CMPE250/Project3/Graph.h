//
// Created by bdk12 on 23.11.2018.
//

#ifndef PROJECT3_GRAPH_H
#define PROJECT3_GRAPH_H

#include <stack>
#include <vector>
#include "Vertex.h"
using namespace std;

class Graph{
public:
    vector<Vertex> vertices;
    vector<Vertex> cracks;
    int counter=1;
    stack<Vertex> myStack;
    Graph();
    Graph(int n);
    Graph(const Graph& g);
    Graph& operator=(const Graph& g);
    ~Graph();
    void scc();
    void scc2(bool isVisited[],Vertex& v);
    void findCracks();



};
#endif //PROJECT3_GRAPH_H
