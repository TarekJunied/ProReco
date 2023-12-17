
from utils import read_log
from scipy import stats
from pm4py.statistics.start_activities.log.get import get_start_activities
import sys
import numpy as np
sys.path.append(
    "/home/qc261227/Recommender/RecommenderSystem/backend/flask_app")


def feature_n_unique_start_activities(log_path):
    log = read_log(log_path)
    log_start = get_start_activities(log)
    return len(log_start)


def feature_start_activities_min(log_path):
    log = read_log(log_path)
    log_start = get_start_activities(log)
    start_activities_occurrences = list(log_start.values())

    return np.min(start_activities_occurrences)


def feature_start_activities_max(log_path):
    log = read_log(log_path)
    log_start = get_start_activities(log)
    start_activities_occurrences = list(log_start.values())

    return np.max(start_activities_occurrences)


def feature_start_activities_mean(log_path):
    log = read_log(log_path)
    log_start = get_start_activities(log)
    start_activities_occurrences = list(log_start.values())

    return np.mean(start_activities_occurrences)


def feature_start_activities_median(log_path):
    log = read_log(log_path)
    log_start = get_start_activities(log)
    start_activities_occurrences = list(log_start.values())

    return np.median(start_activities_occurrences)


def feature_start_activities_std(log_path):
    log = read_log(log_path)
    log_start = get_start_activities(log)
    start_activities_occurrences = list(log_start.values())

    return np.std(start_activities_occurrences)


def feature_start_activities_variance(log_path):
    log = read_log(log_path)
    log_start = get_start_activities(log)
    start_activities_occurrences = list(log_start.values())

    return np.var(start_activities_occurrences)


def feature_start_activities_q1(log_path):
    log = read_log(log_path)
    log_start = get_start_activities(log)
    start_activities_occurrences = list(log_start.values())

    return np.percentile(start_activities_occurrences, 25)


def feature_start_activities_q3(log_path):
    log = read_log(log_path)
    log_start = get_start_activities(log)
    start_activities_occurrences = list(log_start.values())

    return np.percentile(start_activities_occurrences, 75)


def feature_start_activities_iqr(log_path):
    log = read_log(log_path)
    log_start = get_start_activities(log)
    start_activities_occurrences = list(log_start.values())

    return stats.iqr(start_activities_occurrences)


def feature_start_activities_skewness(log_path):
    log = read_log(log_path)
    log_start = get_start_activities(log)
    start_activities_occurrences = list(log_start.values())
    result = stats.skew(start_activities_occurrences)
    if np.isnan(result):
        result = 0
    return 0


def feature_start_activities_kurtosis(log_path):
    log = read_log(log_path)
    log_start = get_start_activities(log)
    start_activities_occurrences = list(log_start.values())
    result = stats.kurtosis(start_activities_occurrences)
    if np.isnan(result):
        result = 0
    return result
