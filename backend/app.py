from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json
from include.square_api import kill_all, tester
from include.database import fetch_all


app = Flask(__name__)
CORS(app, resources={r"/*" : {"origins":"http://localhost:3000"}})
CORS(app, resources={r"/*" : {"origins":"https://connect.squareup.com"}})
kill_all()

@app.route('/get_hello')
def index():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/fetch_all_data', methods=['GET'])
def fetch_all_data():
    return jsonify({"payments" : fetch_all()})

@app.route('/make_payment', methods=['POST'])
def make_payment():
    request_data = request.get_json()
    tester(request_data["value"], request_data["service"])

if __name__ == '__main__':
    app.run(debug=True)

