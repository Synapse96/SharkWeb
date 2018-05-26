from flask import Flask, jsonify, request
from mongoengine import connect
from models import HighSchool


app = Flask(__name__)

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
            print(attendance)
            avg = calculate_avg(attendance)
    return jsonify({'Avg_attendance': avg}), 200


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
            print(enrollments)
            avg = calculate_avg(enrollments)
    return jsonify({'Avg_enrollments': int(avg)}), 200


@app.route("/compare", methods=['GET'])
def compare_schools():
    schools = request.args.get('school_id')
    print(schools)
    connect('high_school')
    average_attendances = {}
    for sid in schools:
        for school in HighSchool.objects(id=int(sid)):
            attendance = list(map(float, school.attendance.values()))
            average_attendances[sid] = calculate_avg(attendance)

    return jsonify(average_attendances), 200


def calculate_avg(l):
    if len(l) != 0:
        avg = sum(l)/len(l)
    else:
        avg = 0
    return avg


if __name__ == '__main__':
    app.run()