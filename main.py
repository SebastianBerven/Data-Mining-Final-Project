import utils
import KNN_Functions as knn
import Naive_Bayes_Functions as bayes
import Decision_Tree_Functions as dtree
import Random_Forest_Functions as rforest
import ARM_Functions as arm

def main():
    test_knn()
    # [County,State,Pov_Pct_All,Median_Income,Crime_Rate_per_100000,Population,Mean_Rent,Pct_Income_as_Rent]

def test_knn():
    data, _ = utils.read_table("combined_data_normalized.csv", True)
    class_index = 4
    predictors = [2,3,5,7]
    results = knn.knn_classifier(data, class_index, predictors, 5, 5)
    accuracy = utils.compute_accuracy(results)
    print(accuracy)
    utils.confusion_matrix(results, "Crime Rate?", "KNN Classifier Prediction of Crime Rate")
    

main()