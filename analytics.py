from flask import Flask, jsonify, request
from flask_cors import CORS
from mongoengine import connect
from models import HighSchool
import statistics as st

app = Flask(__name__)
CORS(app)

connect(
    host='mongodb://admin:comp9321@ds229450.mlab.com:29450/sharkweb'
)


@app.route("/attendance/<sid>", methods=['GET'])
def get_average_attendance(sid):
    response = {}
    connect('high_school')
    avg = 0
    if not HighSchool.objects(id=sid):
        response['error'] = "invalid id in request"
        return jsonify(response), 400
    else:
        for school in HighSchool.objects(id=sid):
            attendance = list(map(float, school.attendance_rates.values()))
            if len(attendance) == 0:
                return jsonify({}), 200
            avg = st.harmonic_mean(attendance)
    return jsonify({'avg_attendance': avg}), 200


@app.route("/enrollments/<sid>", methods=['GET'])
def get_average_enrollments(sid):
    response = {}
    connect('high_school')
    avg = 0
    if not HighSchool.objects(id=sid):
        response['error'] = "invalid id in request"
        return jsonify(response), 400
    else:
        for school in HighSchool.objects(id=sid):
            enrollments = list(map(float, school.enrollments.values()))
            if len(enrollments) == 0:
                return jsonify({}), 200
            avg = st.mean(enrollments)
    return jsonify({'avg_enrollments': int(avg)}), 200


@app.route("/selective-score/<sid>", methods=['GET'])
def avg_min_selective_score(sid):
    response = {}
    connect('high_school')
    avg = -1
    if not HighSchool.objects(id=sid):
        response['error'] = "invalid id in request"
        return jsonify(response), 400
    else:
        for school in HighSchool.objects(id=sid):
            if school.selective == "Not Selective":
                return jsonify({}), 200
            scores = list(map(float, school.selective_entry_scores.values()))
            avg = st.mean(scores)
    return jsonify({'avg_min_selective_scores': int(avg)}), 200


@app.route("/compare-attendances", methods=['GET'])
def compare_attendances():
    schools = request.args.getlist('school_id')
    connect('high_school')
    average_attendances = {}
    for sid in schools:
        for school in HighSchool.objects(id=int(sid)):
            # get the avg attendance_rates
            attendance = list(map(float, school.attendance_rates.values()))
            average_attendances[school.name] = st.harmonic_mean(attendance)

    return jsonify(average_attendances), 200


@app.route("/compare-enrollments", methods=['GET'])
def compare_enrollments():
    schools = request.args.getlist('school_id')
    connect('high_school')
    average_enrollments = {}
    for sid in schools:
        for school in HighSchool.objects(id=int(sid)):
            # get the avg enrolments
            enrollments = list(map(float, school.enrollments.values()))
            average_enrollments[school.name] = st.mean(enrollments)

    return jsonify(average_enrollments), 200


@app.route("/compare-students", methods=['GET'])
def compare_students():
    schools = request.args.getlist('school_id')
    connect('high_school')
    num_students = {}
    for sid in schools:
        for school in HighSchool.objects(id=int(sid)):
            # get current num. of students
            num_students[school.name] = int(school.students)

    return jsonify(num_students), 200


@app.route("/compare-selective-entries", methods=['GET'])
def compare_selective_entry():
    schools = request.args.getlist('school_id')
    connect('high_school')
    average_selective_entry = {}
    for sid in schools:
        for school in HighSchool.objects(id=int(sid)):
            if school.selective != 'Not Selective':
                scores = list(map(float, school.selective_entry_scores.values()))
                average_selective_entry[school.name] = st.mean(scores)

    return jsonify(average_selective_entry), 200


if __name__ == '__main__':
    app.run(port=5003)
