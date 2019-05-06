import utils
import copy
import math

def decision_tree_classifier(table, header, predicted, predictors, k):
    '''
    Reads a table and returns the results.
    Parameter table: The table to be tested.
    Parameter header: Header of table.
    Parameter predicted: Column to be estimated.
    Parameter predictors: List of predictors used to estimate.
    Parameter k: Rounds of tests to be conducted.
    Returns: Results
    '''
    att_domains = compute_domains(predictors, table)
    random_table = utils.shuffle_table(table)
    
    groups = utils.strat_partition(random_table, predicted, k) # Creates equally distributed partitions.
    results = [] # Initializes necessary variables.
    for x in range(k):
        test_set = groups[x]
        train_set = []
        for y in groups[:x] + groups[x+1:]: # Creates test set
            for z in y:
                train_set.append(z)
        
        tree = tdidt(train_set, predictors, att_domains, predicted, header)
        results2 = check_tree(tree, test_set, predicted, header)
        results += results2

    return results

def tdidt(instances, att_indexes, att_domains, class_index, header = None, num = 0):
    tree = ["Attribute"]
    att_index = select_attribute(instances, att_indexes, class_index) # Uses entropy to select split attribute.
    tree.append(header[att_index])
    att_indexes_new = copy.deepcopy(att_indexes) 
    att_indexes_new.remove(att_index)
    partition = partition_instances(instances, att_index, att_domains[att_index]) # Splits on attribute.

    
    for branch in partition:
        if len(partition[branch]) == 0: # Case 3
            tree = make_leaf_node(instances, class_index, num)
            break
        elif has_same_class_label(partition[branch], class_index): # Case 1
            buffer = ["Value", branch, make_leaf_node(partition[branch], class_index, len(instances))]
            tree.append(buffer)
        elif len(att_indexes_new) == 0: # Case 2
            buffer = ["Value", branch, make_leaf_node(partition[branch], class_index, len(instances))]
            tree.append(buffer)        
        else: # No cases, recurse.
            buffer = ["Value", branch, tdidt(partition[branch], att_indexes_new, att_domains, class_index, header, len(instances))]
            tree.append(buffer)
    return tree

def check_tree(tree, test_set, class_index, header):
    results = []
    for item in test_set:
        buffer = [item, 0, item[class_index]] # Formats answer
        answer = traverse_tree(tree, item, header) # Recurses down tree
        buffer[1] = answer
        results.append(buffer)
    return results

def traverse_tree(tree, test, header):
    if tree[0] == "Leaves":
        return tree[1][0]
    else:
        for branch in range(2, 2 + len(tree[2:])):
            if test[header.index(tree[1])] == tree[branch][1]:
                return traverse_tree(tree[branch][2], test, header)

def has_same_class_label(table, class_index):
    return all(table[i][class_index] is table[0][class_index] for i in range(len(table)))

def select_attribute(instances, att_indexes, class_index):
    lowest = [100,0]
    for i in att_indexes:
        _, groups = utils.group_by(instances, i)
        total = 0
        for group in groups:
            E = 0
            _, counts = utils.get_frequencies(group, class_index)
            for j in range(len(counts)):
                proportion = counts[j]/sum(counts)
                E += -(proportion * math.log(proportion, 2))
            E *= len(group)/len(instances)
            total += E
        if total < lowest[0]:
            lowest[0] = total
            lowest[1] = i
    
    return lowest[1]

def partition_instances(instances, att_index, att_domain):
    partition = {}
    for att_value in att_domain:
        subinstances = []
        for instance in instances:
            if instance[att_index] == att_value:
                subinstances.append(instance)
        partition[att_value] = subinstances
    return partition

def make_leaf_node(table, class_index, total):
    values, counts = utils.get_frequencies(table, class_index)
    if total == 0:
        inner = [values[counts.index(max(counts))], len(table), 0, round(len(table)*100, 1)]
    else:
        inner = [values[counts.index(max(counts))], len(table), total, round(len(table)*100/total, 1)]
    buffer = ["Leaves", inner]
    return buffer

def compute_domains(indexes,data):
    domains = {}
    for i in indexes:
        domains[i] = list(set(utils.get_column(data, i)))
    
    return domains