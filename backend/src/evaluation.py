import sys
from utils import get_all_ready_logs,split_data
from recommender import classification
from filehelper import gather_all_xes
from measures import read_target_entries,read_target_entry
from features import read_feature_matrix
from init import init_testing_logs


if __name__ == "__main__":
    sys.setrecursionlimit(5000)
    
    all_log_paths = gather_all_xes("./LogGenerator/logs") + gather_all_xes("../logs/Process_Discovery_Contests/testing") 

    all_ready_logs_paths = get_all_ready_logs(all_log_paths,"token_precision")

    ready_training,ready_testing = split_data(all_ready_logs_paths,0.7)

    x = read_feature_matrix(ready_training)
    
    ready_testing = ready_testing
   
    y = [None]*len(ready_training)
    i = 0
    for log_path in ready_training:
        y[i] = read_target_entry(log_path,"token_precision")
        i += 1

    correct = 0
    for log_path in ready_testing:
        actual = read_target_entry(log_path,"token_precision")
        prediction = classification(log_path, x, y)[0]
        print("ACUTAL: ", actual)
        print("PREDICTION: ", prediction)

        if actual == prediction: 
            correct +=1
            print("Correct")
        else:
            print("Wrong")

    print("TOTAL CORRECT: ", correct)
    print("OUT OF ", len(ready_testing))
    print(correct/len(ready_testing))

   