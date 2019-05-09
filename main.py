import utils
import KNN_Functions as knn
import Naive_Bayes_Functions as bayes
import Decision_Tree_Functions as dtree
import Random_Forest_Functions as rforest
import ARM_Functions as arm
import Data_Visualization as dv
import operator

def main():
    test_knn()
    #test_naive_bayes()
    #test_decision_tree()
    #test_random_forest()
    #do_arm()
    #data_vis()
    #stats()
    # [County,State,Pov_Pct_All,Median_Income,Crime_Rate_per_100000,Population,Mean_Rent,Pct_Income_as_Rent]

def test_knn():
    data, _ = utils.read_table("combined_data_normalized.csv", True)
    class_index = 4
    predictors = [2,3,5,9]
    results = knn.knn_classifier(data, class_index, predictors, 5, 5)
    accuracy = utils.compute_accuracy(results)
    print(accuracy)
    utils.confusion_matrix(results, "Crime Rate?", "KNN Classifier Prediction of Crime Rate")
    
def test_naive_bayes():
    data, header = utils.read_table("combined_data_normalized.csv", True)
    class_index = 4
    predictors = [2,3,5,7]
    results = bayes.naive_bayes_classifier(data, header, 10, class_index, predictors, [2,3,5,9])
    accuracy = utils.compute_accuracy(results)
    print(accuracy)
    utils.confusion_matrix(results, "Crime Rate?", "Naive Bayes Classifier Prediction of Crime Rate")


def test_decision_tree():
    data, header = utils.read_table("combined_data_discretized.csv", True)
    class_index = 4
    predictors = [2,3,5,7]
    results = dtree.decision_tree_classifier(data, header, class_index, predictors, 30)
    accuracy = utils.compute_accuracy(results)
    print(accuracy)
    utils.confusion_matrix(results, "Crime Rate?", "Decision Tree Classifier Prediction of Crime Rate")

def test_random_forest():
    data, header = utils.read_table("combined_data_discretized.csv", True)
    class_index = 4
    predictors = [2,3,5,7]
    results = rforest.random_forest_classifier(data, header, class_index, predictors, 100, 25, 3)
    accuracy = utils.compute_accuracy(results)
    print(accuracy)
    utils.confusion_matrix(results, "Crime Rate?", "Random Forest Classifier Prediction of Crime Rate")

def do_arm():
    data, header = utils.read_table("combined_data_discretized.csv", True)
    rules = arm.Association_Rule_Mining(data, header, minsup=.3, minconf=.95, columns=[2,3,4,5,7])
    utils.rules_pretty_print(rules, "Association Rule Mining for Crime Rate Factors")

def data_vis():
    data, header = utils.read_table("combined_data.csv", True)
    x_data, y_data = utils.get_column(data, 3), utils.get_column(data, 5)
    dv.scatter_plot(x_data, y_data, "Poverty Levels v. Crime Rate", "Poverty Levels (%)", "Crime Rate per 100,000 people", 10, "Poverty_v_Crime_graphed.png", 100, True)
    # values, counts = utils.get_frequencies(data, header.index("Pov_Pct_All"))
    # dv.frequency_diagram(values, counts, "Poverty Distribution in the U.S", "Severity of Poverty", "Number of Counties", "poverty_data_graphed.png")

def stats():
    data, header = utils.read_table("combined_data.csv", True)
    for row in data:
        if row[6] == min([x for x in utils.get_column(data, 6) if x != 0]):
            print(row)

main()