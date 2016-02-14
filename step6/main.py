import zmq
from threading import Thread
from queue import Queue
from flask import Flask, jsonify

application = Flask(__name__)
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://127.0.0.1:5555')


def run_expensive():
    q = Queue()
    t = Thread(target=expensive_operation, args=(q,), daemon=True)
    t.start()
    t.result = q
    return t.result.get()


def expensive_operation(q):
    message = dict(function='expensive_operation',
                   args=())
    socket.send_pyobj(message)
    q.put(socket.recv_pyobj())


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
