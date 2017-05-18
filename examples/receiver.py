from zerocaller.zero_async import ZeroReceiver


def say_hello(payload):
    print('Hello %s!' % payload)


receiver = ZeroReceiver()
receiver.register_handler('hello', say_hello)

receiver.receive_action()
