#include "Node.h"

Node::Node(string _name, float _amount){
    this->name = _name;
    this->amount = _amount;
    this->next = NULL;
}

Node::Node(const Node& node){
    this->name = node.name;
    this->amount = node.amount;
    if(node.next) {
        this->next = new Node(*(node.next));
    }
}

Node& Node::operator=(const Node& node){
    this->name = node.name;
    this->amount = node.amount;
    if(node.next) {
        delete this->next;
        this->next = new Node(*(node.next));
    }
    return *this;
}

Node::Node(Node&& node){
    this->name = move(node.name);
    this->amount = move(node.amount);
    this->next = move(node.next);

    node.name = "";
    node.amount = 0;
    node.next = NULL;

}

Node& Node::operator=(Node&& node){
    this->name = move(node.name);
    this->amount = move(node.amount);
    delete this->next;
    this->next = move(node.next);

    node.name = "";
    node.amount = 0;
    node.next = NULL;
    return *this;
}

Node::~Node(){
    if (next) {
        delete next;
    }
}