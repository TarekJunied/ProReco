import sys
import sklearn
from utils import get_all_ready_logs,split_data
from recommender import classification
from filehelper import gather_all_xes
from measures import read_target_entries,read_target_entry,read_target_vector
from features import read_feature_matrix
from init import init_testing_logs






if __name__ == "__main__":
    sys.setrecursionlimit(5000)

    testing_logpaths = gather_all_xes("../logs/testing/")
    training_logppaths = gather_all_xes("../logs/training/")

    ready_for_testingpaths = get_all_ready_logs(testing_logpaths,"token_precison")
    ready_for_trainingpaths = get_all_ready_logs(training_logppaths,"token_precision")

    y_true = [None]*(len(ready_for_testingpaths))
    y_pred = [None]*(len(ready_for_testingpaths))

    x_train = read_feature_matrix(ready_for_trainingpaths)
    y_train = read_target_vector(ready_for_trainingpaths, "token_precision")
    


    for i in range(len(ready_for_testingpaths)):
        y_true[i] = read_target_entry(ready_for_testingpaths[i],"token_precision")
        y_pred[i] = classification(ready_for_testingpaths[i],x_train, y_train)

    input("wait")

    print("ACCURACY: ",sklearn.metrics.accuracy_score(y_true,y_pred))
    print("AVG PRECISION SCORE: ", sklearn.metrics.average_precision_score(y_true, y_pred))

   