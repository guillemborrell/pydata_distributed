import zmq
from threading import Thread
from queue import Queue
from flask import Flask, jsonify
import uuid

application = Flask(__name__)

context = zmq.Context()


def expensive_operation():
    socket = context.socket(zmq.REQ)
    socket.identity = str(uuid.uuid4()).encode('utf-8')
    socket.connect('tcp://127.0.0.1:5555')

    message = dict(function='expensive_operation',
                   args=())
    socket.send_pyobj(message)
    print("sent message")
    response = socket.recv_pyobj()
    print("recv message")
    socket.close()
    return response


@application.route('/')
def root():
    return jsonify(data='Hello, world!')


@application.route('/expensive')
def expensive():
    result = expensive_operation()
    return jsonify(data=result)


if __name__ == '__main__':
    application.debug = True
    application.run()
