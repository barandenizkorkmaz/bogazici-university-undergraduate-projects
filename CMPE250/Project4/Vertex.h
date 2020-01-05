//
// Created by denizkorkmaz on 14.12.2018.
//

#ifndef PROJECT4_VERTEX_H
#define PROJECT4_VERTEX_H

#include <vector>
#include <forward_list>
#include <utility>
using namespace std;
class Vertex{
public:
    int x;
    int y;
    int height;
    int heightDifference;
    bool isVisited;
    vector<pair<int,int>> neighbors;

    Vertex();
    Vertex(int x_,int y_,int heightDiff_);
    Vertex(const Vertex& v);
    Vertex& operator=(const Vertex& v);
    ~Vertex();
    bool operator<(const Vertex& v)const;
};

#endif //PROJECT4_VERTEX_H
