import numpy as np
import random
import os
import copy
from tabulate import tabulate

def rules_pretty_print(rules, intro):
    '''
    Prints ARM rules.
    Parameter rules: Dictionary of rules.
    Parameter intro: String describing rule set.
    '''
    print()
    print(intro)
    header = ["Association Rule", "Support", "Confidence", "Lift"]
    rule_list = []
    for rule in rules:
        lhs = str(rule["lhs"][0]) # Generates LHS rules.
        if len(rule["lhs"]) > 1:
            for i in range(1, len(rule["lhs"])):
                lhs += (" AND " + str(rule["lhs"][i]))
        rhs = str(rule["rhs"][0]) # Generates RHS rules.
        if len(rule["rhs"]) > 1:
            for i in range(1, len(rule["rhs"])):
                lhs += (" AND " + str(rule["rhs"][i]))
        rule_list.append([lhs + " => " + rhs, rule["support"], rule["confidence"], rule["lift"]]) # Adds statistics.
    print(tabulate(rule_list, header, tablefmt="rst", showindex="always"))

def confusion_matrix(results, class_title, matrix_title):
    '''
    Prints out a confusion matrix.
    Parameter results: Results to be graphed on matrix.
    Parameter class_title: Title of class being evaluated.
    Parameter matrix_title: Matrix title.
    '''
    results = [row[-2:] for row in results]
    unique_values = set()
    for row in results:
        for value in row:
            unique_values.add(value)
    row_header = sorted(list(unique_values))
    entries = len(row_header)
    column_header = [class_title]+row_header+["Total", "Recognition (%)"]
    table = create_matrix(entries, row_header) # Initializes matrices
    table = fill_table(table, results, column_header, row_header) # Fills matrices with data
    
    print(matrix_title)
    print(tabulate(table, column_header, tablefmt="rst"))
    print()

def fill_table(table, data, column_header, row_header):
    '''
    Reads a table and fills in with specified data.
    Parameter table: The table to be filled.
    Parameter data: Data to be put into table.
    Returns: Filled table.
    '''
    for row in data:
        table[row_header.index(row[1])][column_header.index(row[0])] += 1 # Increases count at correct index
    for x in range(len(table)):
        total = sum(table[x][1:]) # Calculates total of actual row
        try:
            recognition = round(table[x][x+1]/total, 4) # Recognition = True Positives / Positives
        except:
            recognition = 0 # Catches if total in row is zero.
        table[x].append(total)
        table[x].append(100*recognition)
    return table

def create_matrix(k, row_header):
    '''
    Initializes a table in matrix format.
    Parameter k: Number of rows and columns in matrix.
    Returns: Table.
    '''
    table = [[0 for i in range(k+1)] for j in range(k)]
    for x in range(len(table)):
        table[x][0] = row_header[x] # Adds row header
    return table

def create_dot_file(tree, destination):
    outfile = open(destination+'.dot', "w+")
    print('graph g {', file=outfile)
    print('\trankdir=TB;', file=outfile)
    buffer = get_tree_below(tree, "0")
    for entry in buffer:
        print("\t"+entry, file = outfile)
    
    print("}", file=outfile)
    os.popen("dot -Tpdf -o "+destination+".pdf "+destination+".dot")
    outfile.close

def get_tree_below(root, num):
    buffer = [root[1]+num+' [label='+root[1]+'][shape=box]']
    length = len(root)
    for i in range(2, length):
        if root[i][2][0] == "Attribute":
            new_add = get_tree_below(root[i][2], num+str(i))
            new_add.append(root[1]+num+' -- '+root[i][2][1]+num+str(i)+' [label="'+str(root[i][1])+'"]')
        elif root[i][2][0] == "Leaves":
            new_add = []
            new_add.append('leaf'+num+str(i)+' [label="'+str(root[i][2][1][0])+'"]')
            new_add.append(root[1]+num+' -- leaf'+num+str(i)+' [label="'+str(root[i][1])+'"]')
        
        buffer += new_add
    
    return buffer

def shuffle_table(table):
    '''
    Randomizes the order of rows in a table.
    Parameter table: Table to be randomized.
    Returns: randomized table.
    '''
    randomized = table[:] # shallow copy
    n = len(randomized)
    for i in range(n):
        # generate a random index to swap with i
        rand_index = random.randrange(0, n) # [0, n)
        # task: do the swap
        randomized[i], randomized[rand_index] = randomized[rand_index], randomized[i]
    return randomized

def strat_partition(table, key, k):
    '''
    Partitions data into equally distributed groups.
    Parameter table: The table to be split.
    Parameter key: The key to group the table on.
    Parameter k: Number of groups to be split into.
    Returns: List of partitions.
    '''
    _, groups = group_by(table, key) # Splits table based on key.
    partitions = [[] for _ in range(k)]
    count = 0
    for x in groups:
        for y in x:
            partitions[count%k].append(y) # Apportions values from groups evenly among partitions.
            count += 1
    return partitions

def holdout_partitions(table, split):
    '''
    Generates holdout partitions.
    Parameter table: Original table.
    Parameter split: Fraction of data to put in training set.
    Returns: Training set, testing set
    '''
    randomized = shuffle_table(table)
    n = len(randomized)
    # compute the split index
    split_index = int(split * n)
    train_set = randomized[:split_index]
    test_set = randomized[split_index:]
    return train_set, test_set

def compute_accuracy(data):
    '''
    Computes an accuracy value from a dataset formatted [Item, Guess, Actual].
    Parameter data: List of data to be compared.
    Returns: Accuracy value to two decimal places.
    '''
    for i in range(len(data)):
        data[i] = data[i][-2:]
    values, _ = get_frequencies(data, 0) # Gets a list of unique values.
    accuracy = 0
    for value in values:
        true_positives, true_negatives = 0, 0
        for row in data:
            if row[0] == value and row[1] == value: # Finds true positives.
                true_positives += 1
            elif row[0] != value and row[1] != value: # Finds true negatives.
                true_negatives += 1
        accuracy += ((true_positives + true_negatives)/len(data))
    accuracy = round(accuracy/len(values), 2) # Calculates accuracy
    return accuracy

def lin_reg(x_data, y_data):
    '''
    Generates linear regression coefficients.
    Parameter x_data: X-axis data.
    Parameter y_data: Y-axis data.
    Returns: m, b, r, stderr values.
    '''
    mean_x = np.mean(x_data) #Finds average of data.
    mean_y = np.mean(y_data)
    m = sum([(x_data[i] - mean_x) * (y_data[i] - mean_y) for i in range(len(x_data))]) / \
                        sum([(x_data[i] - mean_x) ** 2 for i in range(len(x_data))]) 
    #Calculates slope of best fit line.

    b = mean_y - m * mean_x 
    #Calculates y-intercept.
    
    r = sum([(x_data[i] - mean_x) * (y_data[i] - mean_y) for i in range(len(x_data))]) / \
            np.sqrt(sum([(x_data[i] - mean_x) ** 2 for i in range(len(x_data))]) * sum([(y_data[i] - mean_y) ** 2 for i in range(len(x_data))]))
    #Calculates correlation coefficient.

    stderr = np.sqrt(sum([(y_data[i] - (m * x_data[i] + b)) ** 2 for i in range(len(x_data))]) / len(x_data))
    #Calculates standard error.

    return m, b, r, stderr


def group_by(table, column_index, include_only_column_index=None):
    '''
    Splits table into parts based on specified attribute.
    Parameter table: Table to be split.
    Parameter column_index: Column to be grouped on.
    Returns: group_names, groups.
    '''
    # first identify unique values in the column
    group_names = sorted(list(set(get_column(table, column_index))))

    # now, we need a list of subtables
    # each subtable corresponds to a value in group_names
    # parallel arrays
    groups = [[] for name in group_names]
    for row in table:
        # which group does it belong to?
        group_by_value = row[column_index]
        index = group_names.index(group_by_value)
        if include_only_column_index is None:
            groups[index].append(row.copy()) # note: shallow copy
        else:
            groups[index].append(row[include_only_column_index])

    return group_names, groups

            
def read_table(filename, Has_header = False):
    '''
    Reads a .csv file into a table.
    Parameter filename: a string containing the file name.
    Parameter Has_header: Boolean value, True if input file has headers.
    Returns: table, header.
    '''
    table = []
    infile = open(filename, "r")
    lines = infile.readlines()
    for line in lines:
        line = line.strip() #removes whitespace characters
        values = line.split(",") #splits on comma
        convert_to_float(values)
        table.append(values)
    if Has_header:
        header = table.pop(0)
    else:
        header = []


    infile.close()
    return table, header


def write_table(destination, original):
    '''
    Takes a table and writes it to a .csv file.
    Parameter destination: a string containing the desired file name.
    Parameter original: table to be converted.
    '''
    outfile = open(destination, "w+")
    for i in range(len(original)):
        for j in range(len(original[i])-1):
            print(original[i][j], end=",", file = outfile)
        print(original[i][len(original[i])-1], file = outfile)
    outfile.close()


def convert_to_int(values):
    '''
    Coverts all applicable items in a list to ints.
    Parameter values: list to be converted.
    '''
    for i in range(len(values)):
        try:
            numeric_val = int(values[i])
            values[i] = numeric_val
        except ValueError:
            pass

def convert_to_float(values):
    '''
    Coverts all applicable items in a list to ints.
    Parameter values: list to be converted.
    '''
    for i in range(len(values)):
        try:
            numeric_val = float(values[i])
            values[i] = numeric_val
        except ValueError:
            pass


def get_column(table, column_index):
    '''
    Reads a table and returns the specified column.
    Parameter table: The table to be scanned.
    Parameter column_index: Index of column to be scanned.
    Returns: Desired column.
    '''
    column = []
    for row in table:
        if row[column_index] != "NA":
            column.append(row[column_index])

    return column


def get_frequencies(table, column_index):
    '''
    Reads a table and returns a list of values and their frequencies.
    Parameter table: The table to be scanned.
    Parameter column_index: Index of column to be scanned.
    Returns: A list of values and a list of frequencies.
    '''
    column = sorted(get_column(table, column_index))
    values = []
    counts = []

    for value in column:
        if value not in values:
            values.append(value)
            # first time we have seen this value
            counts.append(1)
        else: # we've seen it before, the list is sorted...
            counts[-1] += 1

    return values, counts
