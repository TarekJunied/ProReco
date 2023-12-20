import globals
# from feature_controller import read_optimal_features
from measures import read_measure_entry
from multiobjective import predicted_classification_based_scalarization, predicted_regression_based_scalarization


current_mode = "predicted_regression_based_scalarization"


def final_prediction(log_path_to_predict, measure_weight):
    if current_mode == "predicted_regression_based_scalarization":
        dict = predicted_regression_based_scalarization(log_path_to_predict, "random_forest", measure_weight, [
        ], globals.selected_features, globals.algorithm_portfolio)

    elif current_mode == "predicted_classification_based_scalarization":
        dict = predicted_classification_based_scalarization(log_path_to_predict, "random_forest", measure_weight, [
        ], globals.selected_features, globals.algorithm_portfolio)

    return dict


def finale_schnitstelle_hier():
    return 0


if __name__ == "__main__":
    finale_schnittstelle_hier()
