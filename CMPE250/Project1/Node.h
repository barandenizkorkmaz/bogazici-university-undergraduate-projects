#ifndef NODE_H
#define NODE_H

#include <iostream>
using namespace std;

class Node{
public:
    string name;
    float amount;
    Node* next = NULL;

    Node(string _name, float _amount);
    Node(const Node& node);
    Node& operator=(const Node& node);
    Node(Node&& node);
    Node& operator=(Node&& node);
    ~Node();
};

#endif
