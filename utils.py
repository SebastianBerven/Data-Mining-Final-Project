import numpy as np
import random
import os

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
