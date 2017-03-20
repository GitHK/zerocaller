import pickle
import traceback

import zlib
import zmq

STATUS_ERROR = 'error'
STATUS_OK = 'ok'

KEY_COMMAND = 'command'
KEY_PAYLOAD = 'payload'
KEY_STATUS = 'status'


def send_zipped_pickle(socket, obj, flags=0, protocol=-1):
    """pickle an object, and zip the pickle before sending it"""
    pickled_object = pickle.dumps(obj, protocol)
    compressed = zlib.compress(pickled_object)
    return socket.send(compressed, flags=flags)


def recv_zipped_pickle(socket, flags=0, protocol=-1):
    """inverse of send_zipped_pickle"""
    compressed = socket.recv(flags)
    pickled_object = zlib.decompress(compressed)
    return pickle.loads(pickled_object)


class ZeroAwaiter:
    """ Based on the zermq server that is always waiting for commands to be executed. """

    def __init__(self, port=5566, debug=False):
        """
        Listen for actions from remote requesters.

        :param port: local listening port
        """
        self.port = port
        self.handlers = dict()
        self.debug = debug

    def _process_request(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:%s" % self.port)
        obj = recv_zipped_pickle(socket)
        response = self.handle_incoming_message(obj)
        # ho ricevuto
        send_zipped_pickle(socket, response)
        # ho processato

    def handle_requests_forever(self):
        """ Lock execution and handle requests on this thread from now and forwards. """
        while True:
            self._process_request()

    def handle_request(self):
        """ Execute only one handler and return to thread. """
        self._process_request()

    def register_handler(self, command, handler):
        """ Add a handler to which you must respond """
        self.handlers[command] = handler

    def handle_incoming_message(self, message):
        command = message[KEY_COMMAND]
        payload = message[KEY_PAYLOAD]

        if command not in self.handlers:
            return {KEY_STATUS: STATUS_ERROR, KEY_PAYLOAD: 'Command not registered'}

        try:
            response_payload = self.handlers[command](payload)
            return {KEY_STATUS: STATUS_OK, KEY_PAYLOAD: response_payload}
        except Exception as e:
            trace = traceback.format_exc()
            if self.debug:
                print(trace)
            return {KEY_STATUS: STATUS_ERROR, KEY_PAYLOAD: dict(trace=trace, error=str(e))}


class ZeroRequester:
    """ Based on the zeromq client will send a request to the server and await for a response."""

    def __init__(self, host='localhost', port=5566):
        """
        Initialize the connection to the remote responder.

        :param host: remote host name
        :param port: remote host port
        """
        self.host = host
        self.port = port

    def execute_remotely(self, command, payload):
        """ command is the string identified in the handler register in the ZeroResponder """
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://%s:%s" % (self.host, self.port))
        obj = {KEY_COMMAND: command, KEY_PAYLOAD: payload}
        send_zipped_pickle(socket, obj)
        response = recv_zipped_pickle(socket)

        if response[KEY_STATUS] == STATUS_OK:
            return response[KEY_PAYLOAD]
        else:
            print(">>>\nFROM REMOTE:\n%s<<<\n" % response[KEY_PAYLOAD]['trace'])
            raise Exception("%s: %s" % (response[KEY_STATUS], response[KEY_PAYLOAD]['error']))
