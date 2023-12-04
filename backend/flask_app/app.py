import sys
import secrets
import uuid
import os
import json
import globals
from flask import Flask,  jsonify, session, redirect, render_template, Response, request
from flask_cors import CORS
from flask_session import Session
from utils import read_log
from recommender import final_prediction


def generate_token(length=32):
    # Generate a random token of the specified length
    return secrets.token_hex(length)


def get_logpath_of_session(session_token):
    log_dir = "../logs/frontend"

    log_path = f"{log_dir}/{session_token}.xes"

    return log_path


allowed_origins = [
    "http://139.162.188.197",
    "http://www.proreco.co",
    # Add more origins as needed
]


app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, origins="*", supports_credentials=True)



UPLOAD_FOLDER = '../logs/frontend'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/api/submitWeights", methods=['POST'])
def submit_weights():


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

        return final_prediction(get_logpath_of_session(session_token), measure_weight)
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
