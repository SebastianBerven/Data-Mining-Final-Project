import utils
import itertools

def Association_Rule_Mining(data, header, minsup = 0.25, minconf = 0.8, columns = []):
    '''
    Conducts Association Rule Mining.
    Parameter data: The table to be mined.
    Parameter header: Header of data set.
    Parameter minsup: Minimum support for generating itemsets.
    Parameter minconf: Minimum confidence for generated rules.
    Parameter columns: List of column indexes for desired columns.
    Returns: Dictionary of all rules.
    '''
    if columns == []:
        columns = [x for x in range(len(header))]
    new_header = [header[i] for i in columns]
    new_data = choose_columns(data, columns)
    add_attribute_labels(new_data, new_header)
    rules = apriori(new_data, minsup, minconf)
    return rules

def apriori(table, minsup, minconf):
    supported_itemsets = []
    I = compute_unique_values(table)
    L1 = [[a] for a in I]
    supported_itemsets.append(L1)

    k = 2

    while(True):
        Ck = generate_candidate_set(supported_itemsets[k-2])
        Lk = check_candidate_set(table, Ck, minsup)
        if Lk == []:
            break # Doesn't include empty list in itemsets.
        else:
            supported_itemsets.append(Lk)
            k += 1
    supported_itemsets.pop(0) # Gets rid of singletons.

    rules = generate_apriori_rules(table, supported_itemsets, minconf)
    return rules

def generate_apriori_rules(table, supported_itemsets, minconf):
    rules = []
    
    lhs, rhs = generate_sides(supported_itemsets) # Gets two parallel lists of left and right-hand sides.
    for left, right in zip(lhs, rhs):
        rules.append({"lhs": left, "rhs": right}) # Adds initial dictionary values.
    rules_to_delete = []
    for i in range(len(rules)):
        compute_rule_counts(rules[i], table) # Puts in rule statistics.
        compute_rule_interestingness(rules[i], table)
        if rules[i]["confidence"] < minconf:
            rules_to_delete.append(i) # Tallys rules with low confidence.
    rules_to_delete.sort(reverse = True)
    for i in rules_to_delete:
        rules.pop(i) # Deletes rules with low confidence.

    return rules

def generate_sides(itemsets):
    lhs, rhs = [], []
    for Lk in itemsets:
        max_RHS = len(Lk[0])-1 # Largest number of attributes that can appear on RHS
        for item in Lk:
            for i in range(1, max_RHS+1):
                result = list(itertools.combinations(item, i)) # Gives tuple containingall item combinations.
                for tuple in result:
                    rhs.append(list(tuple))
                    lhs.append([x for x in item if x not in tuple]) # Puts anything not in RHS on LHS.

    return lhs, rhs

def check_candidate_set(original, Lk, minsup):
    correct_set = []
    for item in Lk:
        count = 0
        for row in original:
            if set(item).issubset(row):
                count += 1 # Counts number of rows containing item.
        if count/len(original) >= minsup:
            correct_set.append(item) # Indicates good enough support for item.
    return correct_set

def generate_candidate_set(L_k):
    L_k1 = []
    for A in L_k:
        for B in L_k:
            if A != B and A[0:-1] == B[0:-1]: # Rules for adding something to next candidate set.
                AUB = Union(A, B)
                if((not any([True for x in compute_k_1_subsets(AUB) if x not in L_k])) and (AUB not in L_k1)): # No subsets are missing from previous iteration, and there aren't duplicates.
                    L_k1.append(AUB)
    return L_k1

def compute_k_1_subsets(itemset):
    subsets = []
    for i in range(len(itemset)):
        subsets.append(itemset[:i] + itemset[i + 1:])
    return subsets

def compute_unique_values(table):
    unique_values = set()
    for row in table:
        for value in row:
            unique_values.add(value)

    return sorted(list(unique_values))

def check_row_match(terms, row):
    for term in terms:
        if term not in row:
            return 0
    return 1
    
def compute_rule_interestingness(rule, table):
    compute_rule_counts(rule, table)
    rule["confidence"] = rule["Nboth"] / rule["Nleft"]
    rule["support"] = rule["Nboth"] / rule["Ntotal"]
    rule["completeness"] = rule["Nboth"] / rule["Nright"]
    rule["lift"] = (rule["Nboth"] * rule["Ntotal"]) / (rule["Nleft"] * rule["Nright"])

def compute_rule_counts(rule, table):
    Nleft = Nright = Nboth = 0
    Ntotal = len(table)

    for row in table:
        Nleft += check_row_match(rule["lhs"], row)
        Nright += check_row_match(rule["rhs"], row)
        Nboth += check_row_match(rule["lhs"] + rule["rhs"], row)

    rule["Nleft"] = Nleft
    rule["Nright"] = Nright
    rule["Nboth"] = Nboth
    rule["Ntotal"] = Ntotal

def add_attribute_labels(table, header):
    for row in table:
        for i in range(len(row)):
            label = header[i]
            row[i] = label + "=" + row[i]

def choose_columns(data, indexes):
    new_table = [[] for _ in range(len(data))]
    for i in indexes:
        column = utils.get_column(data, i)
        for row, item in zip(new_table, column):
            row.append(item)
    return new_table

def Union(list1, list2):
    combined = sorted(list(set(list1) | (set(list2))))
    return combined