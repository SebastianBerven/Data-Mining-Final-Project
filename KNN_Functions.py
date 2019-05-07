import utils
import copy
import operator
import numpy as np

def knn_classifier(table, predicted, predictors, test_nums, k = 5):
    '''
    Conducts KNN classifier tests.
    Parameter table: The table to be tested.
    Parameter predicted: Column to be estimated.
    Parameter predictors: List of predictors used to estimate.
    Parameter test_nums: Number of tests to be conducted.
    Parameter k: Amount of nearest neighbors to test.
    '''
    random_table = utils.shuffle_table(table)
    random_table = normalize_table(table, predictors)
    groups = utils.strat_partition(random_table, predicted, test_nums) # Creates equally distributed partitions.
    results = []
    for x in range(test_nums):
        test_set = groups[x]
        train_set = []
        for y in groups[:x] + groups[x+1:]: # Creates test set
            for z in y:
                train_set.append(z)
        results += run_knn_tests(train_set, test_set, k, predicted, predictors)
    return results

def run_knn_tests(training_set, test_set, k, predicted, predictors):
    '''
    Runs KNN tests.
    Parameter training_set: Training data.
    Parameter test_set: Testing data.
    Parameter k: Number of closest neighbors to consider.
    Returns: Test case, guess, actual.
    '''
    closest = []
    for item in test_set:
        test = []
        for row in training_set:
            row.append(euc_distance([item[x] for x in predictors], [row[x] for x in predictors])) # Calculates distance only for last 3 atributes.

        training_set.sort(key=operator.itemgetter(-1)) # Sorts on distance.
        candidates = training_set[:k] # Finds k lowest distances.
        choices, count = utils.get_frequencies(candidates, -5)
        test.append(item)
        test.append(choices[count.index(max(count))]) # Finds most common class
        test.append(item[predicted])
        closest.append(test)

        for row in training_set: # Deletes distance row
            del row[-1]

    return closest

def euc_distance(vector1, vector2):
    squares = 0
    for v1, v2 in zip(vector1, vector2):
        if type(v1) == str and type(v2) == str:
            if v1 != v2:
                squares += 1
        else:
            squares += (v1 - v2)**2
    return np.sqrt(squares)

def normalize_table(table, predictors):
    '''
    Reads a table and adds normalized columns.
    Parameter table: The table to be tested.
    Parameter predictors: List of predictors used to estimate.
    Returns: Normalized table.
    '''
    new_table = copy.deepcopy(table)
    normalized = [[] for _ in predictors]
    for x in predictors:
        column = utils.get_column(new_table, x)
        if all(isinstance(item, int) for item in column) or all(isinstance(item, float) for item in column):
            normalized.append(normalize(column)) # Normalizes and adds each predictor column.
        else:
            normalized.append([])
    
    for i in range(len(new_table)):
        for j in range(len(predictors)):
            if normalized[j] != []:
                new_table[i][predictors[j]] = normalized[j][i]

    return new_table

def normalize(data):
    normalized = []
    for x in data:
        normalized.append((x-min(data))/(max(data)-min(data)))
    return normalized
