import time
import concurrent.futures
from flask import Flask, jsonify

application = Flask(__name__)
executor = concurrent.futures.ProcessPoolExecutor(max_workers=4)


def run_expensive():
    future = executor.submit(expensive_operation)
    return future.result()


def expensive_operation():
    time.sleep(1)
    return 'Hello from a very expensive blocking task.'


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
