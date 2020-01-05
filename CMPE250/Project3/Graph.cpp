//
// Created by bdk12 on 23.11.2018.
//
#include <iostream>
#include "Graph.h"
using namespace std;
    Graph::Graph() {

    }

    Graph::Graph(int n) {
        vertices=vector<Vertex>(n);
        for(int i=1;i<=n;i++){
            Vertex v(i);
            vertices[i-1]=v;
        }
    }

    Graph::Graph(const Graph &g) {
        this->vertices=g.vertices;
    }
    Graph& Graph::operator=(const Graph &g) {
        this->vertices=g.vertices;
        return *this;
    }
    Graph::~Graph() {
    }

    void Graph::scc(){
        bool isVisited[vertices.size()];
        for(vector<Vertex>::iterator itr=vertices.begin();itr!=vertices.end();itr++){
            if(!isVisited[(*itr).value-1]){
                scc2(isVisited,(*itr));
            }
        }
    }

    void Graph::scc2(bool isVisited[], Vertex &v) {
        isVisited[v.value-1]=true;
        v.isVisited=true;
        v.index=v.lowLink=counter;
        counter++;
        myStack.push(v);
        v.onStack=true;
        for(auto itr=v.outEdges.begin();itr!=v.outEdges.end();itr++){
            Vertex& child=vertices[(*itr)-1];
            if(!isVisited[(*itr)-1]){
                scc2(isVisited,child);
                v.lowLink=min(v.lowLink,child.lowLink);
            }
            else if(child.onStack){
                v.lowLink=min(v.lowLink,child.index);
            }
            if(v.lowLink!=v.index) { //SCC Detected
                    int value = myStack.top().value;
                    myStack.top().onStack = false;
                    vertices[value - 1].onStack = false;
                    vertices[value-1].isSource = false;
                    myStack.pop();
                    Vertex &previous = myStack.top();

                    while (!vertices[value - 1].outEdges.empty()) {
                        int toBePushed = vertices[value - 1].outEdges.front();
                        vertices[previous.value - 1].outEdges.push_front(toBePushed);
                        vertices[value - 1].outEdges.pop_front();
                    }

                    while (!vertices[value - 1].inEdges.empty()) {
                        int toBePushed = vertices[value - 1].inEdges.front();
                        vertices[previous.value - 1].inEdges.push_front(toBePushed);
                        vertices[value - 1].inEdges.pop_front();
                    }

                    for(auto it=vertices[previous.value-1].outEdges.begin(); it!=vertices[previous.value-1].outEdges.end();){
                        if(vertices[previous.value-1].lowLink==vertices[(*it)-1].lowLink){
                            vertices[previous.value-1].outEdges.remove((*it++));
                        }
                        else{
                            it++;
                        }
                    }

                    for(auto it=vertices[previous.value-1].inEdges.begin(); it!=vertices[previous.value-1].inEdges.end();){
                        if(vertices[previous.value-1].lowLink==vertices[(*it)-1].lowLink){
                            vertices[previous.value-1].inEdges.remove((*it++));
                        }
                        else{
                            it++;
                        }
                    }
                return;

            }

            int value_=myStack.top().value;
            vertices[value_-1].onStack=false;
            myStack.pop();
            return;

        }

        int value__=myStack.top().value;
        vertices[value__-1].onStack=false;
        myStack.pop();
    }


    void Graph::findCracks() {
        for(vector<Vertex>:: iterator it=vertices.begin();it!=vertices.end();it++){
            if((*it).inEdges.empty() && (*it).isSource){
                this->cracks.push_back((*it));
            }
        }
    }