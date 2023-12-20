

def read_shap_explainer(classification_method, x_train):
    cache_file_path = f"./cache/explainers/{classification_method}.pkl"
    try:
        explainer = load_cache_variable(cache_file_path)
    except Exception as e:

        clf = read_fitted_classifier(
            classification_method, chosen_measure, ready_training)

        if classification_method == "decision_tree" or classification_method == "random_forest":
            explainer = shap.TreeExplainer(clf)
        elif classification_method == "knn" or classification_method == "svm" or classification_method == "logistic_regression":
            explainer = shap.KernelExplainer(clf.predict_proba, x_train)
        elif classification_method == "svm":
            explainer = shap.KernelExplainer(clf.predict_proba, x_train)
        else:
            print("no shap values possible for this classification method")
            sys.exit(-1)

        store_cache_variable(explainer, cache_file_path)

    return explainer


def create_shap_graph(ready_training, ready_testing, classification_method, chosen_measure):
    x_test = read_feature_matrix(ready_testing)
    x_train = read_feature_matrix(ready_training)

    x_test = pd.DataFrame(x_test, columns=globals.selected_features)
    x_train = pd.DataFrame(x_train, columns=globals.selected_features)

    explainer = read_shap_explainer(classification_method, x_train)

    shap_values = explainer.shap_values(x_test)

    plt.clf()

    # Plot the SHAP summary plot
    shap.summary_plot(
        shap_values[1], x_test, feature_names=globals.selected_features, show=False)

    # Save the plot
    storage_dir = "../evaluation/shap"

    plt.savefig(
        f'{storage_dir}/{classification_method}_{chosen_measure}_shap_summary_plot.png')
    plt.show()


def create_lime_graph(measure_name):

    ready_training = get_all_ready_logs(
        gather_all_xes("../logs/training"), measure_name)
    ready_testing = get_all_ready_logs(
        gather_all_xes("../logs/testing"), measure_name)

    # Assume 'model' is your scikit-learn classifier
    x_test = read_feature_matrix(ready_testing)
    x_train = read_feature_matrix(ready_training)

    # x_test = pd.DataFrame(x_test, columns=globals.selected_features)
    # x_train = pd.DataFrame(x_train, columns=globals.selected_features)
    def custom_model_predict(x): return classification(
        x, "autofolio", measure_name, ready_training)

    # Assume 'X_train' is your training data
    explainer = lime_tabular.LimeTabularExplainer(
        x_train, mode="classification")

    # Assume 'X_test[i]' is the instance you want to explain
    explanation = explainer.explain_instance(read_feature_vector(
        ready_testing[0]).values.reshape(1, -1), custom_model_predict)

    # Save the explanation plot as a PNG file
    explanation.save_to_file('lime_explanation_plot.png')
