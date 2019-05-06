import utils
import numpy as np
import math

def naive_bayes_classifier(table, header, k, predicted, predictors, cont_attr = []):
    '''
    Reads a table and returns the specified column.
    Parameter table: The table to be tested.
    Parameter k: Rounds of tests to be conducted.
    Parameter predicted: Column to be estimated.
    Parameter predictors: List of predictors used to estimate.
    Parameter cont_attr: List of which predictors are continuous.
    Returns: Linear regression results, KNN results.
    '''
    random_table = utils.shuffle_table(table)
    
    groups = utils.strat_partition(random_table, predicted, k) # Creates equally distributed partitions.
    results = [] # Initializes necessary variables.
    for x in range(k):
        test_set = groups[x]
        train_set = []
        for y in groups[:x] + groups[x+1:]: # Creates test set
            for z in y:
                train_set.append(z)
            
        bayes_table = create_bayes_table(train_set, header, predicted, predictors, cont_attr)
        results2 = run_bayes_tests(bayes_table, header, test_set, predicted, predictors, cont_attr) # Conducts Bayes test
        results += results2
        
    return results

def create_bayes_table(data, header, Class, Classifiers, cont_attr):
    class_names, classes = utils.group_by(data, Class)
    table = [[name for name in class_names]]
    table[0].insert(0, '')
    for x in Classifiers:
        if cont_attr != [] and x in cont_attr: # Adds a row for continuous attributes if they exist.
            buffer = [[] for _ in range(len(table[0]))]
            buffer[0] = [header[x], header[x]]
            table.append(buffer)
        else:
            values, _ = utils.get_frequencies(data, x)
            for y in values:
                buffer = [0 for _ in range(len(table[0]))] # Pads row with zeroes to start.
                buffer[0] = [header[x], y] # Puts in row header.
                table.append(buffer)
    buffer = [0 for _ in range(len(table[0]))] # Adds row for prior probability.
    buffer[0] = "Prior Probability"
    table.append(buffer)
    table = fill_bayes_table(table, header, classes, cont_attr)
    
    return table

def fill_bayes_table(table, header, class_data, cont_attr):
    total = sum(len(x) for x in class_data)
    for i in range(1, len(table[0])):
        subtotal = len(class_data[i-1]) # Finds amount of instances with certain class.
        current = table[1][0][0] # Current attribute being looked at.
        section = '' # Current attribute section.
        row = 1
        while(row < len(table) - 1): # Loops over every row in Bayes table.
            if current != section:
                values, counts = utils.get_frequencies(class_data[i-1], header.index(current)) # If attribute section changes, finds data for new section.
                section = current # Changes the section.
            if cont_attr != [] and header.index(current) in cont_attr:
                column = utils.get_column(class_data[i-1], header.index(current))
                mean = round(np.mean(column), 2) # Stores gaussian values if attribute is continuous.
                std = round(np.std(column), 2)
                table[row][i] = [mean, std]

            else:
                try:
                    table[row][i] = round(counts[values.index(table[row][0][1])] / subtotal, 2) # Calculates corresponding probability.
                except:
                    table[row][i] = 0 # If there is no test instance
            current = table[row+1][0][0]
            row += 1
        table[row][i] = round(subtotal / total, 2)
    return table

def run_bayes_tests(table, header, test_set, predicted, classifiers, cont_attr):
    solved_set = []
    for item in test_set:
        buffer = []
        buffer.append(item)
        result = calculate_bayes(table, item, header, classifiers, cont_attr) # Finds estimated value.
        buffer.append(result) # Includes guess for the test.
        buffer.append(item[predicted]) # Includes actual value for test.
        solved_set.append(buffer)
    return solved_set

def calculate_bayes(table, test, header, classifiers, cont_attr):
    options = table[0][1:] # Creates list for options and list for the probability of those options.
    results = [0 for _ in range(len(options))]
    for x in range(len(options)):
        answer = 1
        for y in classifiers:
            if cont_attr != [] and y in cont_attr: # Searches for a continuous attribute.
                search_string = [header[y], header[y]]
            else:
                search_string = [header[y], test[y]] # Otherwise, searches for attribute titles.
            for row in table:
                if search_string in row:
                    if cont_attr != [] and y in cont_attr:
                        answer *= gaussian(test[y], row[x+1][0], row[x+1][1]) # Calculates gaussian probability for continuous variables.
                        break
                    else:
                        answer *= row[x+1] # Calculates probability according to the Bayes table.
                        break
        answer *= table[-1][x+1] # Also factors in prior probability.
        results[x] = answer

    return options[results.index(max(results))]

def gaussian(x, mean, sdev):
  first, second = 0, 0
  if sdev > 0:
      first = 1 / (math.sqrt(2 * math.pi) * sdev)
      second = math.e ** (-((x - mean) ** 2) / (2 * (sdev ** 2)))
  return first * second