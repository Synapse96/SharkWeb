from flask import Flask, jsonify, request
from mongoengine import connect
import requests
import urllib.request
import urllib.error
import json
import json.decoder

app = Flask(__name__)

connect(
    host='mongodb://admin:comp9321@ds229450.mlab.com:29450/sharkweb'
)


@app.route('/get', methods=['GET'])
def get_data():
    response = {}
    payload = request.args
    data = requests.get('http://127.0.0.1:5001/nearby', params=payload)
    try:
        response = data.json()
        return jsonify(response), 200
    except json.decoder.JSONDecodeError:
        response["error"] = "invalid arguments in request"
        return jsonify(response), 400


@app.route('/profile/<id>', methods=['GET'])
def get_profile(id):
    url_school = 'http://127.0.0.1:5001/school/' + id
    url_photos = 'http://127.0.0.1:5002/photos/' + id
    try:
        with urllib.request.urlopen(url_school) as school_json:
            school_data = json.load(school_json)
            response = school_data
        with urllib.request.urlopen(url_photos) as photos_json:
            photos_data = json.load(photos_json)
            response["photos"] = photos_data
        return jsonify(response), 200
    except urllib.error.HTTPError:
        response["error"] = "invalid id in request"
        return jsonify(response), 400


if __name__ == '__main__':
    app.run(port=5000)
