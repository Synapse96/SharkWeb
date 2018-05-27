from flask import Flask, jsonify, request
from mongoengine import connect
from models import HighSchool
import statistics as st
import operator as op

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
            avg = st.mean(enrollments)
    return jsonify({'avg_enrollments': int(avg)}), 200


@app.route("/compare", methods=['GET'])
def compare_schools():
    schools = request.args.getlist('school_id')
    connect('high_school')
    average_attendances = {}
    average_enrollments = {}
    num_students = {}
    for sid in schools:
        for school in HighSchool.objects(id=int(sid)):
            # get the avg attendance_rates
            attendance = list(map(float, school.attendance_rates.values()))
            average_attendances[school.name] = st.harmonic_mean(attendance)

            # get the avg enrolments
            enrollments = list(map(float, school.enrollments.values()))
            average_enrollments[school.name] = st.mean(enrollments)

            # get current num. of students
            num_students[school.name] = int(school.students)

    sorted_attendances = sorted(average_attendances.items(), key=op.itemgetter(1), reverse=True)
    sorted_enrollments = sorted(average_enrollments.items(), key=op.itemgetter(1), reverse=True)
    sorted_students = sorted(num_students.items(), key=op.itemgetter(1), reverse=True)

    return jsonify({'attendances': sorted_attendances, 'enrollments': sorted_enrollments,
                    'students': sorted_students}), 200


if __name__ == '__main__':
    app.run(port=5003)
