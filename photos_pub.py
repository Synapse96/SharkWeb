from flask import Flask, jsonify
from mongoengine import connect
from models import HighSchool
import urllib.request
import json

app = Flask(__name__)

connect(host='mongodb://admin:comp9321@ds229450.mlab.com:29450/sharkweb')


@app.route("/school/<id>/photos", methods=['GET'])
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
                  name + '&key=AIzaSyDsGuKG_rDmC4wfLvSrxsWb7HVLx59bi2Y'
            with urllib.request.urlopen(url_textsearch) as textsearch_json:
                textsearch_data = json.load(textsearch_json)
                place_id = textsearch_data["results"][0]["place_id"]
                url_details = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=' +  \
                              place_id + '&key=AIzaSyDsGuKG_rDmC4wfLvSrxsWb7HVLx59bi2Y'
                with urllib.request.urlopen(url_details) as details_json:
                    details_data = json.load(details_json)
                    for photo in details_data["result"]["photos"]:
                        photo_reference = photo["photo_reference"]
                        url_photo = 'https://maps.googleapis.com/maps/api/place/photo?photoreference=' + \
                                    photo_reference + '&sensor=false&maxheight=1600&maxwidth=1600' \
                                                      '&key=AIzaSyDsGuKG_rDmC4wfLvSrxsWb7HVLx59bi2Y'
                        response.append(url_photo)

            return jsonify(response), 200


if __name__ == '__main__':
    app.run()
