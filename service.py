from flask import Flask, jsonify
from mongoengine import connect
from models import HighSchool

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run()