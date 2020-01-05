//
// Created by bdk12 on 23.11.2018.
//
#include "Vertex.h"
using namespace std;

    Vertex::Vertex() {}
    Vertex::Vertex(int value_) {
        this->value=value_;
        this->index=-0;
        this->lowLink=0;
        this->isVisited=false;
        this->onStack=false;
        this->isSource=true;
    }
    Vertex::Vertex(const Vertex &v) {
        this->value=v.value;
        this->index=v.index;
        this->lowLink=v.lowLink;
        this->isVisited=v.isVisited;
        this->onStack=v.onStack;
        this->isSource=v.isSource;
    }
    Vertex& Vertex::operator=(const Vertex &v) {
        this->value=v.value;
        this->index=v.index;
        this->lowLink=v.lowLink;
        this->isVisited=v.isVisited;
        this->onStack=v.onStack;
        this->isSource=v.isSource;
        return *this;
    }
    Vertex::~Vertex() {
        this->value=0;
        this->index=0;
        this->lowLink=0;
        this->isVisited= false;
        this->onStack= false;
        this->isSource=true;
    }

    bool Vertex::operator=(const Vertex &v) const {
        return this->value==v.value;
    }

