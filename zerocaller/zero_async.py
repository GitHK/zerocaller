import traceback

from zerocaller.utils import send_zipped_pickle, recv_zipped_pickle

ACTION = 'command'
PAYLOAD = 'payload'


class ZeroSender:
    """
    Used to send a request to the remote backend to be executed
    """

    def __init__(self, host='127.0.0.1', port=5678, gevent_support=False):
        self.host = host
        self.port = port
        self.gevent_support = gevent_support
        if gevent_support:
            import zmq.green as zmq
        else:
            import zmq

        self.context = zmq.Context()
        self.producer = self.context.socket(zmq.PUSH)
        self.producer.bind("tcp://%s:%s" % (host, port))

    def send_action(self, action, payload):
        message = {
            ACTION: action,
            PAYLOAD: payload
        }
        send_zipped_pickle(self.producer, message)


class ZeroReceiver:
    """
    Used receive an action to process
    """

    def __init__(self, host='127.0.0.1', port=5678, debug=False, gevent_support=False):
        self.host = host
        self.port = port
        self.debug = debug
        self.gevent_support = gevent_support
        if gevent_support:
            import zmq.green as zmq
        else:
            import zmq

        self.context = zmq.Context()
        self.consumer = self.context.socket(zmq.PULL)
        self.consumer.connect("tcp://%s:%s" % (host, port))

        self.handlers = dict()

    def register_handler(self, action, handler):
        self.handlers[action] = handler

    def _handle_action(self, message):
        action = message[ACTION]
        payload = message[PAYLOAD]

        if action not in self.handlers:
            raise ValueError("Action '%s' is not registered" % action)

        try:
            self.handlers[action](payload)
        except Exception:
            trace = traceback.format_exc()
            if self.debug:
                print(trace)

    def receive_action(self):
        self._handle_action(recv_zipped_pickle(self.consumer))

    def receive_forever(self):
        while True:
            self.receive_action()
