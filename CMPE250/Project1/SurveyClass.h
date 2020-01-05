#ifndef PROJECT1_SURVEYCLASS_H
#define PROJECT1_SURVEYCLASS_H

#include "LinkedList.h"
#include <string>
using namespace std;

class SurveyClass {
public:
    SurveyClass();
    SurveyClass(const SurveyClass& other);
    SurveyClass& operator=(const SurveyClass& list);
    SurveyClass(SurveyClass&& other);
    SurveyClass& operator=(SurveyClass&& list);
    ~SurveyClass();

    // Adds a new Node to the linked list or updates the corresponding Node in the linked list
    void handleNewRecord(string _name, float _amount);
    // Calculates and returns the minimum amount of expense.
    // The minimum amount can have up to two decimal points.
    float calculateMinimumExpense();
    // Calculates and returns the maximum amount of expense.
    // The maximum amount can have up to two decimal points.
    float calculateMaximumExpense();
    // Calculates and returns the average amount of expense.
    // The average amount can have up to two decimal points.
    float calculateAverageExpense();

    LinkedList* members = NULL;
};


#endif //PROJECT1_SURVEYCLASS_H
