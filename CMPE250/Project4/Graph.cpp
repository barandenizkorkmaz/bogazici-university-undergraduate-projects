//
// Created by denizkorkmaz on 14.12.2018.
//

#include "Graph.h"
#include <iostream>
using namespace std;
Graph::Graph() {}

Graph::Graph(int x, int y) {
    this->row=x;
    this->col=y;
    this->maxHeight=0;
    map=new Vertex*[row];
    for(int i=0;i<row;i++){
        map[i]=new Vertex[col];
    }
}

Graph::Graph(const Graph &g) {
    this->row=g.row;
    this->col=g.col;
    this->map=g.map;
    this->maxHeight=0;
}

Graph& Graph::operator=(const Graph &g) {
    this->row=g.row;
    this->col=g.col;
    this->map=g.map;
    this->maxHeight=g.maxHeight;
    return *this;
}

Graph::~Graph() {
    this->row=0;
    this->col=0;
    this->maxHeight=0;
    for(int i=0;i<row;i++){
        delete[] map[i];
    }
    delete [] map;
}

void Graph::findHeight(int x1, int y1, int x2, int y2) {
    priorityQueue.push(Vertex(x1-1,y1-1,0));
    while(this->map[x2-1][y2-1].isVisited==false){
        int currentX=priorityQueue.top().x;
        int currentY=priorityQueue.top().y;
        int currentHeightDiff=priorityQueue.top().heightDifference;
        this->maxHeight=max(maxHeight,currentHeightDiff);
        this->map[currentX][currentY].isVisited=true;
        this->priorityQueue.pop();
        for(vector<pair<int,int>>::iterator itr=this->map[currentX][currentY].neighbors.begin();itr!=this->map[currentX][currentY].neighbors.end();itr++){
            int childX=(*itr).first;
            int childY=(*itr).second;
            if(this->map[childX][childY].isVisited==false){
                int currentHeight=this->map[currentX][currentY].height;
                int childHeight=this->map[childX][childY].height;
                priorityQueue.push(Vertex(childX,childY,abs(childHeight-currentHeight)));
            }
        }
    }
}