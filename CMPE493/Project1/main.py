import sys
import numpy as np

#
# REFERENCES:
# 1. https://nlp.stanford.edu/IR-book/html/htmledition/edit-distance-1.html
# 2. https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance#Optimal_string_alignment_distance
#

# Prints the corresponding edit table.
def print_table(str1,str2,editTable):
    str1_list = list(str1)
    str2_list = list(str2)
    str1_list.insert(0,' ')
    str2_list.insert(0,' ')
    height = len(str1_list)
    width = len(str2_list)
    print(' ',end=' ')
    for elem in str2_list:
        print(elem,end=' ')
    print()
    for i in range(height):
        print(str1_list[i],end=' ')
        for j in range(width):
            print(editTable[i][j],end=' ')
        print()

# Prints the corresponding sequence of operations.
def print_seq_operations(seqOperations):
    print("The Sequence of Operations:")
    for i,op in enumerate(seqOperations):
        print('{}: {}'.format(i+1,op))

# Prints the results of an algorithm.
def print_output(str1,str2,isDamerauLevenshtein):
    editTable, editDist = computeLevenshtein(str1,str2) if isDamerauLevenshtein == False else computeDamerauLevenshtein(str1,str2)
    seqOperations = getOperations(str1,str2,editTable,isDamerauLevenshtein)
    title_str = 'The Levenshtein Edit Distance' if isDamerauLevenshtein==False else 'The Damerau-Levenshtein Edit Distance'
    res_str = '{} for transforming {} into {} is: {}'.format(title_str,str1,str2,editDist)
    print(res_str)
    print_table(str1,str2,editTable)
    print_seq_operations(seqOperations)
    print('\n')

# Returns the sequence of operations needed to convert str1 to str2 by backtracking.
def getOperations(str1,str2,matrix,isDamerauLevenshtein):
    i, j = len(str1), len(str2)
    ops_list = list()
    while(not(i == 0 and j == 0)):
        cost = 0 if str1[i-1] == str2[j-1] else 1
        substitution = matrix[i-1][j-1] + cost
        insertion = matrix[i, j-1] + 1
        deletion = matrix[i-1, j] + 1
        transposition = matrix[i-2 , j-2] + cost if (i>1 and j>1 and str1[i-1] == str2[j-2] and str1[i-2] == str2[j-1] and isDamerauLevenshtein==True) else float('inf')
        res_operations = [['substitution',substitution],['insertion',insertion],
                             ['deletion',deletion],['transposition',transposition]]
        sorted_current_operation = sorted(res_operations, key=lambda x: (x[1],x[0]))
        op = sorted_current_operation[0][0]
        cur_op = str()
        if op == 'substitution':
            if cost == 0:
                cur_op = 'Copy {}'.format(str1[i-1])
            else:
                cur_op = 'Replace {} with {}'.format(str1[i-1],str2[j-1])
            i-=1
            j-=1
        elif op == 'insertion':
            cur_op = 'Insert {}'.format(str2[j-1])
            j-=1
        elif op == 'deletion':
            cur_op = 'Delete {}'.format(str1[i-1])
            i-=1
        else: # Transposition
            cur_op = 'Transpose {} with {}'.format(str1[i-2],str2[j-2])
            i-=2
            j-=2
        ops_list.append(cur_op)
    return ops_list[::-1]

# Returns the Levenshtein edit table and Levenshtein edit distance.
def computeLevenshtein(str1,str2):
    levenshtein_matrix = np.zeros((len(str1)+1,len(str2)+1),dtype=int)
    for i in range(len(str1)+1):
        levenshtein_matrix[i,0] = i
    for j in range(len(str2)+1):
        levenshtein_matrix[0,j] = j
    for i in range(1,len(str1)+1):
        for j in range(1,len(str2)+1):
            deletion = levenshtein_matrix[i-1,j] + 1
            insertion = levenshtein_matrix[i,j-1] + 1
            substitution = levenshtein_matrix[i-1,j-1]
            levenshtein_matrix[i,j] = min(deletion,insertion,substitution) if str1[i-1] == str2[j-1] else min(deletion,insertion,(substitution+1))
    return levenshtein_matrix,levenshtein_matrix[len(str1),len(str2)]

# Returns the Damerau-Levenshtein edit table and Damerau-Levenshtein edit distance.
def computeDamerauLevenshtein(str1,str2):
    height = len(str1) + 1
    width = len(str2) + 1
    damerauLevenshteinMatrix = np.zeros((height,width),dtype=int)
    for i in range(height):
        damerauLevenshteinMatrix[i,0] = i
    for j in range(width):
        damerauLevenshteinMatrix[0,j] = j
    for i in range(1,height):
        for j in range(1,width):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            insertion = damerauLevenshteinMatrix[i, j - 1] + 1
            deletion = damerauLevenshteinMatrix[i - 1, j] + 1
            substitution = damerauLevenshteinMatrix[i - 1, j - 1] + cost
            distance = min(deletion, insertion, substitution)
            if(i>1 and j>1 and str1[i-1] == str2[j-2] and str1[i-2] == str2[j-1]):
                distance = min(distance, damerauLevenshteinMatrix[i-2,j-2] + cost) #Transposition
            damerauLevenshteinMatrix[i,j] = distance
    return damerauLevenshteinMatrix, damerauLevenshteinMatrix[len(str1),len(str2)]

str1 = str(sys.argv[1])
str2 = str(sys.argv[2])

print_output(str1,str2,False)
print_output(str1,str2,True)
