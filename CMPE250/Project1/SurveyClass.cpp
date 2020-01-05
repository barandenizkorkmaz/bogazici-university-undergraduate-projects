#include "SurveyClass.h"

SurveyClass::SurveyClass() {
    cout << "SurveyClass constructer executed" << endl;
    /*
    members=nullptr;
     */

    members= new LinkedList();
    members->head= nullptr;
    members->tail= nullptr;
    members->length=0;

}

SurveyClass::SurveyClass(const SurveyClass &other) {
    cout << "SurveyClass copy constructor executed" << endl;
    if(other.members){
        members=new LinkedList(*(other.members));
    }
    this->members->length=other.members->length;
    /*
    this->members->length=other.members->length;
    if(other.members->head){
        this->members->head=new Node(*(other.members->head));
    }
    if(other.members->tail){
        this->members->tail=new Node(*(other.members->tail));
    }
    */
}

SurveyClass& SurveyClass::operator=(const SurveyClass &list) {
    cout << "SurveyClass copy assignment operator executed" << endl;
    if(this->members){
        delete this->members;
    }
    members=new LinkedList(*(list.members));
    this->members->length=list.members->length;
    /*
    this->members->length=list.members->length;
    if(list.members->head){
        delete this->members->head;
        this->members->head=new Node(*(list.members->head));
    }
    if(list.members->tail){
        delete this->members->tail;
        this->members->tail=new Node(*(list.members->tail));
    }
    */
    return *this;
}

SurveyClass::SurveyClass(SurveyClass &&other) {
    cout << "SurveyClass move constructor executed" << endl;
    //members=nullptr;
    this->members=move(other.members);
    other.members->length=0;
    other.members= nullptr;
    //other.members= nullptr;

    /*
    if(other.members){
        delete this->members;
        this->members=new LinkedList(*(other.members));
    }
    this->members->length=move(other.members->length);
    other.members->length=0;
    delete other.members;
    other.members= nullptr;
    /*
    /*
    this->members->length=move(other.members->length);
    if(other.members->head){
        delete this->members->head;
        this->members->head=new Node(*(other.members->head));
    }
    if(other.members->tail){
        //this->tail= nullptr;
        delete this->members->tail;
        this->members->tail=new Node(*(other.members->tail));
    }
    other.members->length=0;
    delete other.members->head;
    other.members->head= nullptr;
    delete other.members->tail;
    other.members->tail= nullptr;
    */
}

SurveyClass& SurveyClass::operator=(SurveyClass &&list) {
    cout << "SurveyClass move assignment operator executed" << endl;
    delete this->members;
    this->members=move(list.members);
    list.members->length=0;
    list.members= nullptr;
    /*
    this->members->length=0;
    delete this->members;
    this->members= nullptr;
    //this->members->length=move(list.members->length);
    if(list.members){
        this->members=new LinkedList(*(list.members));
    }
    this->members->length=move(list.members->length);

    list.members=0;
    delete list.members;
    list.members= nullptr;
    */
    /*
    this->members->length=0;
    delete this->members->head;
    delete this->members->tail;

    this->members->length=move(list.members->length);
    if(list.members->head){
        this->members->head=new Node(*(list.members->head));
    }
    if(list.members->tail){
        this->members->tail=new Node(*(list.members->tail));
    }

    list.members->length=0;
    delete list.members->head;
    list.members->head= nullptr;
    delete list.members->tail;
    list.members->tail= nullptr;
    */
    return *this;
}

SurveyClass::~SurveyClass() {
    cout << "SurveyClass destructor executed" << endl;
    delete members;
    members= nullptr;

    //delete members;
    //delete members->head;
    //delete members->tail;

    /*
    members->head= nullptr;
    delete members->head;
     */
}

void SurveyClass::handleNewRecord(string _name, float _amount) {
    if(this->members->head== nullptr){
        this->members->pushTail(_name,_amount);
        return;
    }
    bool isExist=false;
    Node* current=members->head;
    //int size=members->length;
    while(current->next){
        if(current->name == _name){
            isExist=true;
        }
        current=current->next;
    }
    if(current->name == _name){
        isExist=true;
    }
    if(isExist){
        members->updateNode(_name,_amount);
    }
    else{
        members->pushTail(_name,_amount);
    }
}

float SurveyClass::calculateMinimumExpense() {
    float minExp;

    if(members->head== nullptr){
        return 0.0;
    }
    minExp=members->head->amount;
    Node* current=members->head;
    while(current->next){
        if(current->amount<minExp){
            minExp=current->amount;
        }
        current=current->next;
    }
    if(current->amount<minExp){
        minExp=current->amount;
    }
    int temp=minExp*100;
    float finalResult=temp;
    finalResult=finalResult/100;
    return finalResult;
}

float SurveyClass::calculateMaximumExpense() {
    float maxExp;
    if(members->head== nullptr){
        return 0;
    }
    maxExp=members->head->amount;
    Node* current=members->head;
    while(current->next){
        if(current->amount>maxExp){
            maxExp=current->amount;
        }
        current=current->next;
    }
    if(current->amount>maxExp){
        maxExp=current->amount;
    }
    int temp=maxExp*100;
    float finalResult=temp;
    finalResult=finalResult/100;
    return finalResult;
}

float SurveyClass::calculateAverageExpense() {
    float avgExp;
    float totalExp=0;
    Node* current=members->head;
    while(current->next){
        totalExp+=current->amount;
        current=current->next;
    }
    totalExp+=current->amount;
    avgExp=totalExp/(members->length);
    int temp=avgExp*100;
    float finalResult=temp;
    finalResult=finalResult/100;
    return finalResult;
}
