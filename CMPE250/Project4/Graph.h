//
// Created by denizkorkmaz on 14.12.2018.
//

#ifndef PROJECT4_GRAPH_H
#define PROJECT4_GRAPH_H

#include <vector>
#include <queue>
#include "Vertex.h"
using namespace std;

class Graph{
public:
    Vertex** map;
    priority_queue<Vertex> priorityQueue;
    int row;
    int col;
    int maxHeight;

    Graph();
    Graph(int x,int y);
    Graph(const Graph& g);
    Graph& operator=(const Graph& g);
    ~Graph();

    void findHeight(int x1,int y1,int x2,int y2);
};

#endif //PROJECT4_GRAPH_H
