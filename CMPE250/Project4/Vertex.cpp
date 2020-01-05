//
// Created by denizkorkmaz on 14.12.2018.
//

#include "Vertex.h"
using namespace std;

Vertex::Vertex() {
    this->height=0;
    this->isVisited=false;
}

Vertex::Vertex(int x_,int y_,int heightDiff_){
    this->x=x_;
    this->y=y_;
    this->height=0;
    this->heightDifference=heightDiff_;
    this->isVisited=false;
}

Vertex::Vertex(const Vertex &v) {
    this->x=v.x;
    this->y=v.y;
    this->height=v.height;
    this->heightDifference= v.heightDifference;
}
Vertex& Vertex::operator=(const Vertex &v) {
    this->x=v.x;
    this->y=v.y;
    this->heightDifference= v.heightDifference;
    return *this;
}
Vertex::~Vertex() {
    this->x=0;
    this->y=0;
    this->height=0;
    this->heightDifference=0;
    this->isVisited=false;
}

bool Vertex::operator<(const Vertex& v)const{
    return this->heightDifference>v.heightDifference;
}