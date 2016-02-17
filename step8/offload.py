import zmq
import time
import pickle
import sys

context = zmq.Context()


class RpcHandler(object):
    # Dead simple RPC handler
    def __init__(self, conn_string, label):
        self.socket = context.socket(zmq.REQ)
        self.socket.identity = label.encode('utf-8')
        self.socket.connect(conn_string)

    def rpc_listener(self):
        # Initiate the worker by sending a ready signal
        self.socket.send(b'READY')
        while True:
            client, empty, data = self.socket.recv_multipart()
            message = pickle.loads(data)
            result = getattr(self, message['function'])(*message['args'])
            self.socket.send_multipart([client, empty, pickle.dumps(result)])

    @staticmethod
    def expensive_operation():
        time.sleep(1)
        return 'Hello from a very expensive blocking task.'


if __name__ == '__main__':

    runner = RpcHandler("tcp://127.0.0.1:5556", sys.argv[1])
    while True:
        runner.rpc_listener()
