from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# db 커넥트
from flaskext.mysql import


if __name__ == '__main__':
    app.run()
