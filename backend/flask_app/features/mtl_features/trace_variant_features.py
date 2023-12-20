from utils import read_log
from scipy import stats
from pm4py.statistics.traces.generic.log import case_statistics
import sys
import numpy as np
import math
sys.path.append(
    "/home/qc261227/Recommender/RecommenderSystem/backend/flask_app")


def get_occurrences(log_path):
    log = read_log(log_path)
    variants_count = case_statistics.get_variant_statistics(log)
    variants_count = sorted(
        variants_count, key=lambda x: x["count"], reverse=True)
    occurrences = [x["count"] for x in variants_count]
    return occurrences


def feature_ratio_most_common_variant(log_path):
    log = read_log(log_path)
    occurrences = get_occurrences(log_path)
    return sum(occurrences[:1]) / len(log)


def feature_ratio_top_1_variants(log_path):
    log = read_log(log_path)
    occurrences = get_occurrences(log_path)
    len_occurr = len(occurrences)
    len_log = len(log)
    return sum(occurrences[: int(len_occurr * 0.01)]) / len_log


def feature_ratio_top_5_variants(log_path):
    log = read_log(log_path)
    occurrences = get_occurrences(log_path)
    len_occurr = len(occurrences)
    len_log = len(log)
    return sum(occurrences[: int(len_occurr * 0.05)]) / len_log


def feature_ratio_top_10_variants(log_path):
    log = read_log(log_path)
    occurrences = get_occurrences(log_path)
    len_occurr = len(occurrences)
    len_log = len(log)
    return sum(occurrences[: int(len_occurr * 0.1)]) / len_log


def feature_ratio_top_20_variants(log_path):
    log = read_log(log_path)
    occurrences = get_occurrences(log_path)
    len_occurr = len(occurrences)
    len_log = len(log)
    return sum(occurrences[: int(len_occurr * 0.2)]) / len_log


def feature_ratio_top_50_variants(log_path):
    log = read_log(log_path)
    occurrences = get_occurrences(log_path)
    len_occurr = len(occurrences)
    len_log = len(log)
    return sum(occurrences[: int(len_occurr * 0.5)]) / len_log


def feature_ratio_top_75_variants(log_path):
    log = read_log(log_path)
    occurrences = get_occurrences(log_path)
    len_occurr = len(occurrences)
    len_log = len(log)
    return sum(occurrences[: int(len_occurr * 0.75)]) / len_log


def feature_mean_variant_occurrence(log_path):
    occurrences = get_occurrences(log_path)
    return np.mean(occurrences)


def feature_std_variant_occurrence(log_path):
    occurrences = get_occurrences(log_path)
    return np.std(occurrences)


def feature_skewness_variant_occurrence(log_path):
    occurrences = get_occurrences(log_path)
    result = stats.skew(occurrences)
    if np.isnan(result) or math.isnan(result):
        return 0


def feature_kurtosis_variant_occurrence(log_path):
    occurrences = get_occurrences(log_path)
    result = stats.kurtosis(occurrences)
    if math.isnan(result) or np.isnan(result):
        return 0
    return result
