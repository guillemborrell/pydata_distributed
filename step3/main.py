import time
import concurrent.futures
from flask import Flask, jsonify

application = Flask(__name__)


@application.route('/')
def root():
    return jsonify(data='Hello, world!')


@application.route('/expensive')
def expensive():
    time.sleep(1)
    return jsonify(data='Hello from a very expensive and blocking task.')


if __name__ == '__main__':
    application.debug = True
    application.run()
