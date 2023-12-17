from utils import read_log
from scipy import stats
from pm4py.algo.filtering.log.attributes import attributes_filter
import sys
import numpy as np
sys.path.append(
    "/home/qc261227/Recommender/RecommenderSystem/backend/flask_app")


def feature_n_unique_activities(log_path):
    log = read_log(log_path)
    activities = attributes_filter.get_attribute_values(log, "concept:name")
    return len(activities)


def feature_activities_min(log_path):
    log = read_log(log_path)
    activities = attributes_filter.get_attribute_values(log, "concept:name")
    activities_occurrences = list(activities.values())

    return np.min(activities_occurrences)


def feature_activities_max(log_path):
    log = read_log(log_path)
    activities = attributes_filter.get_attribute_values(log, "concept:name")
    activities_occurrences = list(activities.values())

    return np.max(activities_occurrences)


def feature_activities_mean(log_path):
    log = read_log(log_path)
    activities = attributes_filter.get_attribute_values(log, "concept:name")
    activities_occurrences = list(activities.values())

    return np.mean(activities_occurrences)


def feature_activities_median(log_path):
    log = read_log(log_path)
    activities = attributes_filter.get_attribute_values(log, "concept:name")
    activities_occurrences = list(activities.values())

    return np.median(activities_occurrences)


def feature_activities_std(log_path):
    log = read_log(log_path)
    activities = attributes_filter.get_attribute_values(log, "concept:name")
    activities_occurrences = list(activities.values())

    return np.std(activities_occurrences)


def feature_activities_variance(log_path):
    log = read_log(log_path)
    activities = attributes_filter.get_attribute_values(log, "concept:name")
    activities_occurrences = list(activities.values())

    return np.var(activities_occurrences)


def feature_activities_q1(log_path):
    log = read_log(log_path)
    activities = attributes_filter.get_attribute_values(log, "concept:name")
    activities_occurrences = list(activities.values())

    return np.percentile(activities_occurrences, 25)


def feature_activities_q3(log_path):
    log = read_log(log_path)
    activities = attributes_filter.get_attribute_values(log, "concept:name")
    activities_occurrences = list(activities.values())

    return np.percentile(activities_occurrences, 75)


def feature_activities_iqr(log_path):
    log = read_log(log_path)
    activities = attributes_filter.get_attribute_values(log, "concept:name")
    activities_occurrences = list(activities.values())

    return stats.iqr(activities_occurrences)


def feature_activities_skewness(log_path):
    log = read_log(log_path)
    activities = attributes_filter.get_attribute_values(log, "concept:name")
    activities_occurrences = list(activities.values())
    result = stats.skew(activities_occurrences)
    if np.isnan(result):
        result = 0
    return result


def feature_activities_kurtosis(log_path):
    log = read_log(log_path)
    activities = attributes_filter.get_attribute_values(log, "concept:name")
    activities_occurrences = list(activities.values())
    result = stats.kurtosis(activities_occurrences)
    if np.isnan(result):
        result = 0
    return 0
