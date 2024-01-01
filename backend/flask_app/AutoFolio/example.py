import numpy as np
import os
from autofolio.facade.af_csv_facade import AFCsvFacade
import sys
sys.path.append("/rwthfs/rz/cluster/home/qc261227/Recommender/RecommenderSystem/backend/flask_app")
from autofolio_interface import create_feature_csv,create_performance_csv
from filehelper import gather_all_xes, get_all_ready_logs_multiple
from features import space_out_feature_vector_string


def execute():

    os.chdir("../")
    training_log_paths = get_all_ready_logs_multiple(gather_all_xes("../logs/training"))
    testing_log_paths = get_all_ready_logs_multiple(gather_all_xes("../logs/testing"))

    perf_fn = "perf.csv"
    feat_fn = "feats.csv"

    create_feature_csv(training_log_paths,f"./AutoFolio/{feat_fn}")
    create_performance_csv(training_log_paths,f"runtime",f"./AutoFolio/{perf_fn}")
  
    list_of_np_feature_vecs = []
    for log_path in testing_log_paths:
        list_of_np_feature_vecs += [np.fromstring(space_out_feature_vector_string(log_path),sep= " ")]
    

    # will be created (or overwritten) by AutoFolio
    model_fn = "./af_predictors/af_model.pkl"

    os.chdir("./AutoFolio")
    af = AFCsvFacade(perf_fn=perf_fn, feat_fn=feat_fn,objective="runtime",maximize=False,seed=123)


    # fit AutoFolio; will use default hyperparameters of AutoFolio
    af.fit()

    # tune AutoFolio's hyperparameter configuration for 4 seconds
    config = af.tune(wallclock_limit=1000)

    # evaluate configuration using a 10-fold cross validation
    score = af.cross_validation(config=config)

    # re-fit AutoFolio using the (hopefully) better configuration
    # and save model to disk
    af.fit(config=config, save_fn=model_fn)


    for feature_vec in list_of_np_feature_vecs:
        input(AFCsvFacade.load_and_predict(vec=feature_vec, load_fn=model_fn))



if __name__ == "__main__":
    execute()