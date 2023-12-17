import os
from utils import read_log
from scipy import stats
from pm4py.algo.filtering.log.variants import variants_filter
import sys
import numpy as np
sys.path.append(
    "/home/qc261227/Recommender/RecommenderSystem/backend/flask_app")


def feature_n_traces(log_path):
    log = read_log(log_path)
    return len(log)


def feature_n_unique_traces(log_path):
    log = read_log(log_path)
    variants = variants_filter.get_variants(log)
    return len(variants)


def feature_ratio_unique_traces_per_trace(log_path):
    log = read_log(log_path)
    variants = variants_filter.get_variants(log)
    return len(variants) / len(log)
