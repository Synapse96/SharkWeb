from flask import Flask, jsonify, request
from flask_cors import CORS
from mongoengine import connect
import requests
import json
import json.decoder

app = Flask(__name__)
CORS(app)

connect(
    host='mongodb://admin:comp9321@ds229450.mlab.com:29450/sharkweb'
)


@app.route('/schools', methods=['GET'])
def get_schools():
    response = {}
    query = request.query_string.decode("utf-8")
    url = 'http://127.0.0.1:5001/nearby?' + query
    data = requests.get(url)
    try:
        response = jsonify(data.json())
        return after_request(response), 200
    except json.decoder.JSONDecodeError:
        response["error"] = "invalid arguments in request"
        return after_request(jsonify(response)), 400


@app.route('/profile/<id>', methods=['GET'])
def get_profile(id):
    response = {}
    url_school = 'http://127.0.0.1:5001/school/' + id
    url_photos = 'http://127.0.0.1:5002/photos/' + id
    url_attendance = 'http://127.0.0.1:5003/attendance/' + id
    url_enrollments = 'http://127.0.0.1:5003/enrollments/' + id
    url_selective_scores = 'http://127.0.0.1:5003/selective-score/' + id
    school_data = requests.get(url_school)
    photos_data = requests.get(url_photos)
    attendance_data = requests.get(url_attendance)
    enrollments_data = requests.get(url_enrollments)
    selective_scores_data = requests.get(url_selective_scores)
    try:
        response = school_data.json()
        response["photos"] = photos_data.json()
        response.update(attendance_data.json())
        response.update(enrollments_data.json())
        response.update(selective_scores_data.json())
        return jsonify(response), 200
    except json.decoder.JSONDecodeError:
        response["error"] = json.decoder.JSONDecodeError
        return after_request(jsonify(response)), 400


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


if __name__ == '__main__':
    app.run(port=5000)
