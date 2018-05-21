from flask import Flask
from mongoengine import connect

app = Flask(__name__)


@app.route('/')
def index():
    # TODO: return high school locations for map or search bar from database of NSW High Schools
    return 'Hello World!'


@app.route('/profile/<name>')
def profile(name):
    # TODO: given the name return the profile of the NSW High School if it exists
    return 'NSW High School Profile'


if __name__ == '__main__':
    connect(host='mongodb://admin:comp9321@ds229450.mlab.com:29450/sharkweb')
    app.run()
