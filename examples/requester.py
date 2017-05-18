from zerocaller import ZeroRequester

requester = ZeroRequester()


def make_request(name):
    result = requester.execute_remotely('say_hello', name)
    print(result)


make_request('World,')
make_request('how')
make_request('are')
make_request('you?')
