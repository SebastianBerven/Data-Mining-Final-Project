import utils
import Decision_Tree_Functions as dtree
import random
import operator

def random_forest_classifier(data, header, predicted, predictors, N, M, F):
    '''
    Reads a table and returns the accuracy and results.
    Parameter data: The table to be tested.
    Parameter header: Header of table.
    Parameter predicted: Column to be estimated.
    Parameter predictors: List of predictors used to estimate.
    Parameter N: Number of decision trees to be created.
    Parameter M: Number of best decision trees to be chosen.
    Parameter F: Number of attributes to use for each tree.
    Returns: Results
    '''
    random_table = utils.shuffle_table(data)
    groups = utils.strat_partition(random_table, predicted, 3) # Creates equally distributed partitions.
    remainder_set = groups[0]+groups[1]
    test_set = groups[2]
    forest = random_forest(data, predictors, predicted, remainder_set, header, N, M, F)
    results = check_forest(test_set, predicted, forest, header)
    
    return results

def random_forest(full_table, att_choices, class_index, remainder, header, N, M, F):
    forest_trees = []
    for _ in range(N):
        att_indexes = sorted(random.sample(att_choices, k=F))
        train_set, test_set = generate_bagging(remainder)
        att_domains = dtree.compute_domains(att_indexes, full_table)
        tree = dtree.tdidt(train_set, att_indexes, att_domains, class_index, header)
        results = dtree.check_tree(tree, test_set, class_index, header)
        accuracy = utils.compute_accuracy(results)
        forest_trees.append([tree, accuracy])
    forest_trees.sort(key=operator.itemgetter(-1), reverse=True)
    best_trees = []
    for item in forest_trees[:M]:
        best_trees.append(item[0])
    return best_trees

def check_forest(test_set, class_index, forest, header):
    results = []
    for item in test_set:
        buffer = [item, None, item[class_index]]
        choices = []
        for tree in forest:
            answer = dtree.check_tree(tree, [item], class_index, header)
            choices.append(answer[0][1])
    
        buffer[1] = max(set(choices), key=choices.count)

        results.append(buffer)

    return results

def generate_bagging(data):
    train_set, test_set = [], []
    random_set = random.choices(data, k=len(data))
    for item in random_set:
        if item not in train_set:
            train_set.append(item)
    for item in data:
        if item not in train_set:
            test_set.append(item)

    if len(test_set) == 0:
        test_set.append(train_set.pop(1))
    
    return train_set, test_set

