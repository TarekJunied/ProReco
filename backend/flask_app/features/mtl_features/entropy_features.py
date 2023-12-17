from utils import read_log
from scipy import stats
from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.algo.filtering.log.end_activities import end_activities_filter
import subprocess
import os
import sys
import numpy as np
sys.path.append(
    "/home/qc261227/Recommender/RecommenderSystem/backend/flask_app")

single_args = ["-f", "-p", "-B", "-z"]
double_args = ["-d", "-r"]


def default_call(log_path, arg1, arg2, arg3):
    output = subprocess.run(
        [
            "java",
            "-jar",
            f"{os.getcwd()}/mtl_features/eventropy.jar",
            arg1,
            arg2,
            arg3,
            f"{log_path}",
        ],
        capture_output=True,
        text=True,
    )
    if len(output.stdout) == 0:
        return 0
    return float(output.stdout.strip().split(":")[1])


def feature_entropy_trace(log_path):
    return default_call(log_path, "-f", "", "")


def feature_entropy_prefix(log_path):
    return default_call(log_path, "-p", "", "")


def feature_entropy_global_block(log_path):
    return default_call(log_path, "-B", "", "")


def feature_entropy_lempel_ziv(log_path):
    return default_call(log_path, "-z", "", "")


def feature_entropy_k_block_diff_1(log_path):
    return default_call(log_path, "-d", "1", "")


def feature_entropy_k_block_diff_3(log_path):
    return default_call(log_path, "-d", "3", "")


def feature_entropy_k_block_diff_5(log_path):
    return default_call(log_path, "-d", "5", "")


def feature_entropy_k_block_ratio_1(log_path):
    return default_call(log_path, "-r", "1", "")


def feature_entropy_k_block_ratio_3(log_path):
    return default_call(log_path, "-r", "3", "")


def feature_entropy_k_block_ratio_5(log_path):
    return default_call(log_path, "-r", "5", "")


def feature_entropy_knn_3(log_path):
    return default_call(log_path, "-k", "3", "1",)


def feature_entropy_knn_5(log_path):
    return default_call(log_path, "-k", "5", "1")


def feature_entropy_knn_7(log_path):
    return default_call(log_path, "-k", "7", "1")
