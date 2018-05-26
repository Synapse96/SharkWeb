from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from mongoengine import connect
from models import HighSchool

app = Flask(__name__)
CORS(app)

connect(
    host='mongodb://admin:comp9321@ds229450.mlab.com:29450/sharkweb'
)


@app.route("/nearby", methods=['GET'])
def get_nearby_schools():
    lat = request.args.get("lat")
    long = request.args.get("long")
    radius = float(request.args.get("radius"))
    connect('high_school')
    # get all schools within the radius given
    schools = HighSchool.objects(loc__geo_within_sphere=[(long, lat), radius/6371])
    locations = []
    for school in schools:
        loc_dict = school.loc
        loc_dict['id'] = school.id
        locations.append(loc_dict)

    return locations, 200


@app.route("/school/<id>", methods=['GET'])
def get_school_profile(id):
    response = []
    connect('high_school')
    if not HighSchool.objects(id=id):
        response = "invalid id in request"
        ret = Response(response)
        return after_request(ret), 400
    else:
        for school in HighSchool.objects(id=id):
            response.append(school.to_json())
            ret = Response(response)
            return after_request(ret), 200


@app.route("/school", methods=['GET'])
def filter_schools():
    selective = request.args.get("selective")
    gender = request.args.get("gender")

    response = []
    connect('high_school')
    if selective and gender:
        for schools in HighSchool.objects(selective=selective, gender=gender):
            response.append(dict(schools.to_mongo()))
    elif selective:
        for schools in HighSchool.objects(selective=selective):
            response.append(dict(schools.to_mongo()))
    elif gender:
        for schools in HighSchool.objects(gender=gender):
            response.append(dict(schools.to_mongo()))
    else:
        response.append({"error": "invalid arguments in request"})

    return jsonify(response), 200


# Add CORS header on response header
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


if __name__ == '__main__':
    app.run()
