from flask import Flask, jsonify
from mongoengine import connect
import urllib.request
import urllib.error
import json

app = Flask(__name__)

connect(
    host='mongodb://admin:comp9321@ds229450.mlab.com:29450/sharkweb'
)


@app.route('/')
def index():
    # TODO: return high school locations for map or search bar from database of NSW High Schools
    return 'Hello World!'


@app.route('/profile/<id>')
def profile(id):
    response = {}
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
