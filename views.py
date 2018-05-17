from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    # return high school locations for map or search bar from database of
    # NSW High Schools
    return 'Hello World!'


@app.route('/profile/<name>')
def profile(name):
    # given the name return the profile of the NSW High School if it exists
    return 'NSW High School Profile'


if __name__ == '__main__':
    app.run()
