import time
from threading import Thread
from queue import Queue
from flask import Flask, jsonify

application = Flask(__name__)


def run_expensive():
    q = Queue()
    t = Thread(target=expensive_operation, args=(q,), daemon=True)
    t.start()
    t.result = q
    return t.result.get()


def expensive_operation(q):
    time.sleep(1)
    q.put('Hello from a very expensive blocking task.')


@application.route('/')
def root():
    return jsonify(data='Hello, world!')


@application.route('/expensive')
def expensive():
    result = run_expensive()
    return jsonify(data=result)


if __name__ == '__main__':
    application.debug = True
    application.run()
