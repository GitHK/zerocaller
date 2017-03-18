from zerocaller import ZeroRequester

requester = ZeroRequester()
result = requester.execute_remotely('say_hello', 'world')

print(result)
