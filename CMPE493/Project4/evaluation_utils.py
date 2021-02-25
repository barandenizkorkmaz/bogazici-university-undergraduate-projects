import random

"""
Returns macro-averaged precision and precision values for separate classes.
Arguments:
    actual:
        List of actual labels
        Type: list(int)
    predicted:
        List of predicted labels
        Type: list(int)
Returns:
    tuple:
        macro-averaged precision:
            Type: float
        precision values for separate classes:
            Type: list(float)
"""
def precision(actual:list, predicted:list)->tuple:
    labels = [0,1]
    precisions = list()
    for label in labels:
        tp = 0
        fp = 0
        for y_actual, y_predicted in zip(actual,predicted):
            if y_predicted == label:
                if y_actual == label:
                    tp += 1
                else:
                    fp += 1
        precisions.append(float(tp)/(tp+fp))
    averagePrecision = sum(precisions) / len(precisions)
    return averagePrecision, precisions

"""
Returns macro-averaged recall and recall values for separate classes.
Arguments:
    actual:
        List of actual labels
        Type: list(int)
    predicted:
        List of predicted labels
        Type: list(int)
Returns:
    tuple:
        macro-averaged recall:
            Type: float
        recall values for separate classes:
            Type: list(float)
"""
def recall(actual:list, predicted:list)->tuple:
    labels = [0, 1]
    recalls = list()
    for label in labels:
        tp = 0
        fn = 0
        for y_actual, y_predicted in zip(actual, predicted):
            if y_actual == label:
                if y_predicted == label:
                    tp += 1
                else:
                    fn += 1
        recalls.append(float(tp)/(tp+fn))
    averageRecall = sum(recalls) / len(recalls)
    return averageRecall, recalls

"""
Returns macro-averaged f-measure and f-measure values for separate classes.
Arguments:
    actual:
        List of actual labels
        Type: list(int)
    predicted:
        List of predicted labels
        Type: list(int)
Returns:
    tuple:
        macro-averaged f-measure:
            Type: float
        f-measure values for separate classes:
            Type: list(float)
"""
def f1_score(actual:list, predicted:list)->tuple:
    _precision, _precisions = precision(actual, predicted)
    _recall, _recalls = recall(actual, predicted)
    labels = [0, 1]
    f1_scores = list()
    for label in labels:
        precisionLabel = _precisions[label]
        recallLabel = _recalls[label]
        f1_scores.append(2.0*precisionLabel*recallLabel/(precisionLabel+recallLabel))
    return sum(f1_scores)/len(f1_scores), f1_scores

"""
Returns p-value result of Approximate Randomization Test.
Arguments:
    y_actual:
        List of actual labels
        Type: list(int)
    y_predicted1:
        List of predicted labels by Model 1.
        Type: list(int)
    y_predicted2:
        List of predicted labels by Model 2.
        Type: list(int)
    R:
        Number of iterations. By default 1000.
        Type: int
Returns:
    p-value:
        Type: float
"""
def approximateRandomizationTest(y_actual:list, y_predicted1:list, y_predicted2:list, R=1000) -> float:
    print("Approximate Randomization Test")
    counter = 0
    f1_1, _ = f1_score(y_actual, y_predicted1)
    f1_2, _ = f1_score(y_actual, y_predicted2)
    s = abs(f1_1 - f1_2)
    for i in range(R):
        y_predicted1Tmp = y_predicted1
        y_predicted2Tmp = y_predicted2
        for j in range(len(y_actual)):
            a = y_predicted1Tmp[j]
            b = y_predicted2Tmp[j]
            rnd = random.randint(0,1)
            if rnd == 1:
                y_predicted1Tmp[j] = b
                y_predicted2Tmp[j] = a
        f1_1_tmp, _ = f1_score(y_actual, y_predicted1Tmp)
        f1_2_tmp, _ = f1_score(y_actual, y_predicted2Tmp)
        s_test = abs(f1_1_tmp - f1_2_tmp)
        if s_test >= s:
            counter += 1
    p = float(counter + 1)/(R + 1)
    print("p: {}".format(p))
    return p