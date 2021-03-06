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
    school_size = request.args.get("school_size")
    min_selective = request.args.get("min_selective_score")
    min_attendance = request.args.get("attendance_rate")
    genders = request.args.getlist("gender")
    category = request.args.getlist("category")
    connect('high_school')
    # get all schools within the radius given
    schools = HighSchool.objects(loc__geo_within_sphere=[(float(long), float(lat)), radius/6371],
                                 students__gte=int(school_size), gender__in=genders, selective__in=category)

    locations = []
    for school in schools:
        attendance = school.attendance_rates.get('2017')
        if attendance == 'na' or float(attendance) < float(min_attendance):
            continue
        selective_score = school.selective_entry_scores.get('2018')
        if school.selective != 'Not Selective' and (
                'na' in selective_score or float(selective_score) < float(min_selective)):
            continue
        loc_dict = school.loc
        loc_dict['id'] = school.id
        loc_dict['name'] = school.name
        loc_dict['address'] = school.street + ", " + school.suburb
        locations.append(loc_dict)
    resp = jsonify(locations)
    return resp, 200


@app.route("/school/<id>", methods=['GET'])
def get_school_profile(id):
    response = []
    connect('high_school')
    if not HighSchool.objects(id=id):
        response = "invalid id in request"
        ret = Response(response)
        return ret, 400
    else:
        for school in HighSchool.objects(id=id):
            response.append(school.to_json())
            ret = Response(response)
            return ret, 200


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


if __name__ == '__main__':
    app.run(port=5001)
