from utils import read_log
from scipy import stats
import sys
import numpy as np
sys.path.append(
    "/home/qc261227/Recommender/RecommenderSystem/backend/flask_app")


def get_trace_length_list(log_path):
    log = read_log(log_path)
    trace_lengths = []
    n_events = 0
    for trace in log:
        n_events += len(trace)
        trace_lengths.append(len(trace))
    return trace_lengths


def compute_trace_length_histogram(log_path):
    log = read_log(log_path)
    trace_lengths = [len(trace) for trace in log]
    histogram, _ = np.histogram(trace_lengths, bins=10, density=True)
    return histogram


def feature_n_events(log_path):
    log = read_log(log_path)
    n_events = 0
    for trace in log:
        n_events += len(trace)

    return n_events


def feature_trace_len_min(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return np.min(trace_lengths)


def feature_trace_len_max(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return np.max(trace_lengths)


def feature_trace_len_mean(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return np.mean(trace_lengths)


def feature_trace_len_median(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return np.median(trace_lengths)


def feature_trace_len_mode(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return stats.mode(trace_lengths)[0]


def feature_trace_len_std(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return np.std(trace_lengths)


def feature_trace_len_variance(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return np.var(trace_lengths)


def feature_trace_len_q1(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return np.percentile(trace_lengths, 25)


def feature_trace_len_q3(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return np.percentile(trace_lengths, 75)


def feature_trace_len_iqr(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return stats.iqr(trace_lengths)


def feature_trace_len_geometric_mean(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return stats.gmean(trace_lengths)


def feature_trace_len_geometric_std(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return stats.gstd(trace_lengths)


def feature_trace_len_harmonic_mean(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return stats.hmean(trace_lengths)


def feature_trace_len_skewness(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return stats.skew(trace_lengths)


def feature_trace_len_kurtosis(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return stats.kurtosis(trace_lengths)


def feature_trace_len_coefficient_variation(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return stats.variation(trace_lengths)


def feature_trace_len_entropy(log_path):
    trace_lengths = get_trace_length_list(log_path)
    return stats.entropy(trace_lengths)


def compute_trace_length_histogram(log):
    trace_lengths = [len(trace) for trace in log]
    histogram, _ = np.histogram(trace_lengths, bins=10, density=True)
    return histogram


def feature_trace_len_hist1(log_path):
    log = read_log(log_path)
    histogram = compute_trace_length_histogram(log)
    return histogram[0]


def feature_trace_len_hist2(log_path):
    log = read_log(log_path)
    histogram = compute_trace_length_histogram(log)
    return histogram[1]


def feature_trace_len_hist3(log_path):
    log = read_log(log_path)
    histogram = compute_trace_length_histogram(log)
    return histogram[2]


def feature_trace_len_hist4(log_path):
    log = read_log(log_path)
    histogram = compute_trace_length_histogram(log)
    return histogram[3]


def feature_trace_len_hist5(log_path):
    log = read_log(log_path)
    histogram = compute_trace_length_histogram(log)
    return histogram[4]


def feature_trace_len_hist6(log_path):
    log = read_log(log_path)
    histogram = compute_trace_length_histogram(log)
    return histogram[5]


def feature_trace_len_hist7(log_path):
    log = read_log(log_path)
    histogram = compute_trace_length_histogram(log)
    return histogram[6]


def feature_trace_len_hist8(log_path):
    log = read_log(log_path)
    histogram = compute_trace_length_histogram(log)
    return histogram[7]


def feature_trace_len_hist9(log_path):
    log = read_log(log_path)
    histogram = compute_trace_length_histogram(log)
    return histogram[8]


def feature_trace_len_hist10(log_path):
    log = read_log(log_path)
    histogram = compute_trace_length_histogram(log)
    return histogram[9]


def feature_trace_len_skewness_hist(log_path):
    trace_lengths = get_trace_length_list(log_path)
    trace_len_hist, _ = np.histogram(trace_lengths, density=True, bins=10)
    return stats.skew(trace_len_hist)


def feature_trace_len_kurtosis_hist(log_path):
    trace_lengths = get_trace_length_list(log_path)
    trace_len_hist, _ = np.histogram(trace_lengths, density=True,  bins=10)
    return stats.kurtosis(trace_len_hist)
