from utils import read_log
from scipy import stats
from pm4py.statistics.end_activities.log.get import get_end_activities
import sys
import numpy as np
sys.path.append(
    "/home/qc261227/Recommender/RecommenderSystem/backend/flask_app")


def feature_n_unique_end_activities(log_path):
    log = read_log(log_path)
    log_end = get_end_activities(log)
    return len(log_end)


def feature_end_activities_min(log_path):
    log = read_log(log_path)
    log_end = get_end_activities(log)
    end_activities_occurrences = list(log_end.values())

    return np.min(end_activities_occurrences)


def feature_end_activities_max(log_path):
    log = read_log(log_path)
    log_end = get_end_activities(log)
    end_activities_occurrences = list(log_end.values())

    return np.max(end_activities_occurrences)


def feature_end_activities_mean(log_path):
    log = read_log(log_path)
    log_end = get_end_activities(log)
    end_activities_occurrences = list(log_end.values())

    return np.mean(end_activities_occurrences)


def feature_end_activities_median(log_path):
    log = read_log(log_path)
    log_end = get_end_activities(log)
    end_activities_occurrences = list(log_end.values())

    return np.median(end_activities_occurrences)


def feature_end_activities_std(log_path):
    log = read_log(log_path)
    log_end = get_end_activities(log)
    end_activities_occurrences = list(log_end.values())

    return np.std(end_activities_occurrences)


def feature_end_activities_variance(log_path):
    log = read_log(log_path)
    log_end = get_end_activities(log)
    end_activities_occurrences = list(log_end.values())

    return np.var(end_activities_occurrences)


def feature_end_activities_q1(log_path):
    log = read_log(log_path)
    log_end = get_end_activities(log)
    end_activities_occurrences = list(log_end.values())

    return np.percentile(end_activities_occurrences, 25)


def feature_end_activities_q3(log_path):
    log = read_log(log_path)
    log_end = get_end_activities(log)
    end_activities_occurrences = list(log_end.values())

    return np.percentile(end_activities_occurrences, 75)


def feature_end_activities_iqr(log_path):
    log = read_log(log_path)
    log_end = get_end_activities(log)
    end_activities_occurrences = list(log_end.values())

    return stats.iqr(end_activities_occurrences)


def feature_end_activities_skewness(log_path):
    log = read_log(log_path)
    log_end = get_end_activities(log)
    end_activities_occurrences = list(log_end.values())
    result = stats.skew(end_activities_occurrences)
    if np.isnan(result):
        result = 0
    return result


def feature_end_activities_kurtosis(log_path):
    log = read_log(log_path)
    log_end = get_end_activities(log)
    end_activities_occurrences = list(log_end.values())
    result = stats.kurtosis(end_activities_occurrences)
    if np.isnan(result):
        result = 0
    return result
