import pickle
import zlib


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