## Algorithm Recommender System (ALORS)

Uses collaborative filtering to recommend algorithms
- solves matrix completion problem, where given performance data is incomplete
- addresses cold start problem, i.e. predicting/selecting algorithms for new (unseen) problem instances


# Requirements

- This program is compatible with Python 2.7
- Requires the following packages to run: numpy, scipy, sklearn

- For memory-based matrix completion, ARS.jar is called, so > java 1.6 is required
- For model-based matrix completion, i.e. CofiRank, cofirank-deploy is provided (this executable is generated under Linux)


# Example run setting

A dictionary like as follows should be provided to run alors.py
You can find all the tested cases (available in the "as_datasets" folder) under dataset_dict_all.py 

    exp_setting_dict = {'ai_file_path': main_folder_path + "/SAT11_HAND-ai-perf.csv", ## Algorithm-Instance performance data file
                        'ft_file_path': main_folder_path + "/SAT11_HAND-features.txt", ## Instance feature file
                        'cv_file_path': main_folder_path + "/SAT11_HAND-cv.txt",  ## Cross-validation data: if this is not given, folds will be automatically generated wrt num_splits
                        'perf_bound_val': 5000, ## Performance value bound (e.g. runtime limit for SAT.. ignore if you don't have such limit) 
                        'eval_metrics': [EvaluationMetricType.ParX, EvaluationMetricType.RatioSolved, EvaluationMetricType.Rank], ## performance metrics to evaluate / report
                        'mf_type': MatrixFactorizationType.svd, ## matrix factorisation method to extract latent features
                        'mf_rank': 10, ## matrix rank for matrix factorisation
                        'higher_better': False,  ## whether higher values in given performance data mean better or not
                        'map_method': MappingMethodType.RandomForest, ## mapping method to be used between initial descriptive features and latent features for cold start  
                        'num_splits': 10, ## Number of splits for cross-validation... isn't used if a cross-validation file is given   
                         }