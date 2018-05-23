from flask import Flask, jsonify, request
from flask_cors import CORS
from mongoengine import connect
from models import HighSchool

app = Flask(__name__)
CORS(app)

connect(
    host='mongodb://admin:comp9321@ds229450.mlab.com:29450/sharkweb'
)


@app.route("/school/<id>", methods=['GET'])
def get_school_profile(id):
    response = {}
    connect('high_school')
    if not HighSchool.objects(id=id):
        response['error'] = "invalid id in request"
        return jsonify(response), 400
    else:
        for school in HighSchool.objects(id=id):
            response = dict(school.to_mongo())
            return jsonify(response), 200


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
    app.run()