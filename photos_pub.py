from flask import Flask, jsonify
from flask_cors import CORS
from mongoengine import connect
from models import HighSchool
import urllib.request
import json

app = Flask(__name__)
CORS(app)

connect(host='mongodb://admin:comp9321@ds229450.mlab.com:29450/sharkweb')


@app.route("/photos/<id>", methods=['GET'])
def get_photos(id):
    response = []
    connect('high_school')
    if not HighSchool.objects(id=id):
        response = "invalid id in request"
        return jsonify(response), 400
    else:
        for school in HighSchool.objects(id=id):
            name = school.name.replace(' ', '%20')
            url_textsearch = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + \
                  name + '&key=AIzaSyBqleXsttoPMyDVWDMQgcYwutB7ENx4icQ'
            with urllib.request.urlopen(url_textsearch) as textsearch_json:
                textsearch_data = json.load(textsearch_json)
                if textsearch_data["status"] != "OK":
                    response = []
                    return jsonify(response), 200
                place_id = textsearch_data["results"][0]["place_id"]
                url_details = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=' +  \
                              place_id + '&key=AIzaSyBqleXsttoPMyDVWDMQgcYwutB7ENx4icQ'
                with urllib.request.urlopen(url_details) as details_json:
                    details_data = json.load(details_json)
                    if 'photos' in details_data["result"]:
                        for photo in details_data["result"]["photos"]:
                            photo_reference = photo["photo_reference"]
                            url_photo = 'https://maps.googleapis.com/maps/api/place/photo?photoreference=' + \
                                        photo_reference + '&sensor=false&maxheight=1600&maxwidth=1600' \
                                                          '&key=AIzaSyBqleXsttoPMyDVWDMQgcYwutB7ENx4icQ'
                            response.append(url_photo)

            return jsonify(response), 200


if __name__ == '__main__':
    app.run(port=5002)
