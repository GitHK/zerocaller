from zerocaller import ZeroRequester

zero_requester = ZeroRequester()
result = zero_requester.execute_remotely('say_hello', 'world')

print(result)
