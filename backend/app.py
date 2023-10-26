import sys
import secrets
import uuid
import os
import json
import pm4py
from flask import Flask,  jsonify, session, redirect, render_template, Response, request
from flask_cors import CORS
from flask_session import Session
from src.utils import read_log
from src.recommender import classification_test
sys.path.append("src")


project_root = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, project_root)


def generate_token(length=32):
    # Generate a random token of the specified length
    return secrets.token_hex(length)


def get_logpath_of_session(session_token):
    log_dir = "./logs/frontend"

    log_path = f"{log_dir}/{session_token}.xes"

    return log_path


app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)  # Add this line to enable CORS for your app


@app.route("/api/submitWeights", methods=['POST'])
def submit_weights():

    if request.method == 'POST':
        print(request.data)

        json_data = request.data.decode('utf-8')

        parsed_data = json.loads(json_data)

        slider_values = parsed_data['requestData']['sliderValues']
        session_token = parsed_data['requestData']['sessionToken']
        print("nice slider values: ", slider_values)
        print("soon we will make use of them")

        return classification_test(get_logpath_of_session(session_token), "token_precision")
    else:
        return "This route only accepts POST requests."


UPLOAD_FOLDER = './logs/frontend'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/api/submitLog", methods=['POST'])
def submit_log():
    if request.method == 'POST':
        if 'xesFile' not in request.files:

            return "No file part"

        file = request.files['xesFile']

        if file.filename == '':
            return "No selected file"

        if file:
            session_token = str(uuid.uuid4())

            file.filename = f"{session_token}.xes"

            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

            file.save(filename)

            session['session_token'] = session_token

            return jsonify({'sessionToken': session_token})
    return "This route only accepts POST requests"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
