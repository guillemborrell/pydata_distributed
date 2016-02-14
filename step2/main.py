import time
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def root():
    return jsonify(data='Hello, world!')


@app.route('/expensive')
def expensive():
    time.sleep(1)
    return jsonify(data='Hello from a very expensive and blocking task.')


if __name__ == '__main__':
    app.debug = True
    app.run()
