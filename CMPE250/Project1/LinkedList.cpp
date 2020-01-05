
#include "LinkedList.h"

LinkedList::LinkedList() {
    cout << "LinkedList constructor executed" << endl;
    this->head=nullptr;
    this->tail=nullptr;
    this->length=0;
}

LinkedList::LinkedList(const LinkedList &list) {
    cout << "LinkedList copy constructor executed" << endl;
    //does this copy constructor needs freeing some data???
    this->length=list.length;
    if(list.head){
        //this->head= nullptr;
        this->head=new Node(*(list.head));
    }
    if(list.tail){
        //this->tail= nullptr;
        this->tail=new Node(*(list.tail));
    }
}

LinkedList& LinkedList::operator=(const LinkedList &list) {
    cout << "LinkedList copy assignment operator executed" << endl;
    this->length=list.length;
    if(list.head){
        //this->head= nullptr;
        delete this->head;
        this->head=new Node(*(list.head));
    }
    if(list.tail){
        //this->tail= nullptr;
        delete this->tail;
        this->tail=new Node(*(list.tail));
    }
    return *this;
}

LinkedList::LinkedList(LinkedList &&list) {
    cout << "LinkedList move constructor executed" << endl;
    this->length=move(list.length);

    if(list.head){
        delete this->head;
        this->head=new Node(*(list.head));
    }
    if(list.tail){
        //this->tail= nullptr;
        delete this->tail;
        this->tail=new Node(*(list.tail));
    }

    list.length=0;
    delete list.head;
    list.head= nullptr;
    delete list.tail;
    list.tail= nullptr;
}

LinkedList& LinkedList::operator=(LinkedList &&list) {
    cout << "LinkedList move assignment operator executed" << endl;
    this->length=0;
    delete this->head;
    delete this->tail;

    this->length=move(list.length);

    if(list.head){
        this->head=new Node(*(list.head));
    }
    if(list.tail){
        this->tail=new Node(*(list.tail));
    }

    list.length=0;
    delete list.head;
    list.head= nullptr;
    delete list.tail;
    list.tail= nullptr;

    return *this;
}

LinkedList::~LinkedList() {
    cout << "LinkedList destructor executed" << endl;
    head=nullptr;
    delete head;
}

void LinkedList::pushTail(string _name, float _amount) {
    Node* newNode=new Node(_name,_amount);

    if (head==nullptr) {
        head = newNode;
        tail = head;
        length++;
        return;
    }
    Node *current = head;
    while (current->next != nullptr) {
        current = current->next;
    }
    current->next = newNode;
    tail = newNode;
    length++;
}

void LinkedList::updateNode(string _name, float _amount) {
    Node* current=head;
    while(current->name!=_name){
        current=current->next;
    }
    current->amount=_amount;
}

void LinkedList::print() {
    if(head==nullptr){
        cout << "The list is empty!" << endl;
    }
    else {
        Node *current = head;
        while (current->next != nullptr) {
            cout << current->amount << " ";
            current = current->next;
        }
        cout << current->amount << endl;
    }
}