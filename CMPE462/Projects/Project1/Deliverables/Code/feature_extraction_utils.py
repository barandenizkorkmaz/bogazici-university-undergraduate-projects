import numpy as np

THRESHOLD_BRIGHTNESS = 0.8
THRESHOLD_DARKNESS = -0.7

def darkness_distribution_analysis(MATRIX):
    result = []
    for row in MATRIX:
        consecutive = 0
        current_consecutive = []
        for element in row:
            if element < THRESHOLD_DARKNESS:
                consecutive += 1
            else:
                current_consecutive.append(consecutive)
                consecutive = 0
        if len(current_consecutive) == 0:
            continue
        first_darkness_size = current_consecutive[0]
        last_darkness_size = current_consecutive[-1]
        result.append(abs(last_darkness_size-first_darkness_size))
    return np.std(result)

def brightness_distribution_analysis(MATRIX):
    result = []
    for row in MATRIX:
        current_row = []
        for i in range(len(row)):
            if row[i]>=THRESHOLD_BRIGHTNESS:
                current_row.append(i)
        if len(current_row) == 0:
            continue
        else:
            result.append(np.average(current_row))
    return np.std(result)