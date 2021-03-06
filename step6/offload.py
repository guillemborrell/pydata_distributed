import zmq
import time

context = zmq.Context()


class RpcHandler(object):
    # Dead simple RPC handler
    def __init__(self, conn_string):
        self.socket = context.socket(zmq.REP)
        self.socket.bind(conn_string)

    def rpc_listener(self):
        print('Wait for message')
        message = self.socket.recv_pyobj()
        print('Got message')
        result = getattr(self, message['function'])(*message['args'])
        self.socket.send_pyobj(result)

    @staticmethod
    def expensive_operation():
        time.sleep(1)
        return 'Hello from a very expensive blocking task.'


if __name__ == '__main__':

    runner = RpcHandler("tcp://127.0.0.1:5555")
    while True:
        runner.rpc_listener()
