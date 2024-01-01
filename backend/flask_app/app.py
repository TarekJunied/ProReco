import sys
import secrets
import uuid
import os
import json
import globals
import logging

from flask import Flask,  jsonify, session, redirect, render_template, Response, request, send_file
from flask_cors import CORS
from flask_session import Session
from utils import read_log
from recommender import final_prediction, get_final_petri_net_dict, create_random_log_dict, get_regressed_algo_measure_dict, get_decision_plot_dict
from feature_controller import get_total_feature_functions_dict


globals.measures_list = ["token_precision",
                         "token_fitness", "generalization", "pm4py_simplicity"]
globals.algorithm_portfolio = [
    "alpha", "inductive", "heuristic", "split", "ILP"]
globals.selected_features = list(get_total_feature_functions_dict().keys())


def generate_token(length=32):
    # Generate a random token of the specified length
    return secrets.token_hex(length)


def get_logpath_of_session(session_token):
    log_dir = "../logs/frontend"

    log_path = f"{log_dir}/{session_token}.xes"

    return log_path


allowed_origins = [
    "http://139.162.188.197",
    "http://139.162.188.197",
    "https://proreco.co",
    "http://proreco.co",
    "*"
    # Add more origins as neede
]
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(24)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


UPLOAD_FOLDER = '../logs/frontend'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.before_request
@app.before_request
def log_request_info():
    logger.info(f"New request: {request.method} {request.path}")
    logger.info(f"Headers: {request.headers}")
    logger.info(f"Body: {request.get_data(as_text=True)}")


@app.route("/api/submitWeights", methods=['POST'])
def submit_weights():
    app.logger.info(f"Received POST request at /api/submitWeights: {request.data}")

    if request.method == 'POST':
        print(request.data)

        json_data = request.data.decode('utf-8')

        parsed_data = json.loads(json_data)

        slider_values = parsed_data['requestData']['sliderValues']
        session_token = parsed_data['requestData']['sessionToken']

        measure_weight = {}
        i = 0
        for measure in globals.measures_list:
            measure_weight[measure] = slider_values[i]
            i += 1

        log_path_to_predict = get_logpath_of_session(session_token)
        prediction_score_dict = final_prediction(
            log_path_to_predict, measure_weight)
        algo_measure_dict = get_regressed_algo_measure_dict(
            log_path_to_predict)

        print("returning the following string jsonified for the post request submitWeights")
        print({'predictonDict': prediction_score_dict,
              "algoMeasureDict": algo_measure_dict})
        return jsonify({'predictonDict': prediction_score_dict, "algoMeasureDict": algo_measure_dict})
    else:
        return "This route only accepts POST requests."


@app.route("/api/submitLog", methods=['POST'])
def submit_log():
    if request.method == 'POST':
        if 'xesFile' not in request.files:

            return "No file part"

        file = request.files['xesFile']

        if file.filename == '':
            return "No selected file"

        if file:
            print("file received", file)
            session_token = str(uuid.uuid4())

            file.filename = f"{session_token}.xes"

            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

            file.save(filename)

            session['session_token'] = session_token

            return jsonify({'sessionToken': session_token})
    return "This route only accepts POST requests"


@app.route("/api/requestModel", methods=['POST'])
def request_model():

    if request.method == 'POST':
        print(request.data)

        json_data = request.data.decode('utf-8')

        parsed_data = json.loads(json_data)

        discovery_algorithm = parsed_data['requestData']['discoveryAlgorithm']
        session_token = parsed_data['requestData']['sessionToken']

        log_path_to_predict = get_logpath_of_session(session_token)

        return jsonify(get_final_petri_net_dict(log_path_to_predict, discovery_algorithm))
    else:
        return "This route only accepts POST requests."


@app.route("/api/progress", methods=['POST'])
def get_progress():
    if request.method == 'POST':

        json_data = request.data.decode('utf-8')

        parsed_data = json.loads(json_data)

        session_token = parsed_data['requestData']['sessionToken']

        ret_dict = globals.get_progress_dict_of_session_token(session_token)

        # ret_dict = globals.progress_dict[session_token]

        return jsonify(ret_dict), 200


@app.route("/api/generateLog", methods=['POST'])
def request_log_generation():
    app.logger.info(f"Received POST request at /api/submitWeights: {request.data}")

    if request.method == 'POST':
        print(request.data)

        json_data = request.data.decode('utf-8')

        parsed_data = json.loads(json_data)

        slider_values = parsed_data['requestData']

        session_token = str(uuid.uuid4())

        log_path = get_logpath_of_session(session_token)

        globals.set_progress_state(log_path, "start")

        create_random_log_dict(slider_values, session_token)

        session['session_token'] = session_token

        return jsonify({'sessionToken': session_token})
    else:
        return "This route only accepts POST requests."


@app.route('/api/downloadEventLog')
def download_file():
    # Get the session token from the headers
    session_token = request.headers.get('Authorization')

    log_path = get_logpath_of_session(session_token)
    return send_file(log_path, as_attachment=True)


@app.route('/api/getExplainationDict', methods=['POST'])
def get_explaination_dict():
    if request.method == 'POST':

        json_data = request.data.decode('utf-8')

        parsed_data = json.loads(json_data)

        session_token = parsed_data['requestData']['sessionToken']

        log_path_to_explain = get_logpath_of_session(session_token)

        ret_dict = get_decision_plot_dict(log_path_to_explain)

        return jsonify(ret_dict), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
