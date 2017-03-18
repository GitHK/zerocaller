from zerocaller import ZeroAwaiter


def say_hello_handler(payload):
    return "Hello %s!" % payload


zero_responder = ZeroAwaiter()
zero_responder.register_handler('say_hello', say_hello_handler)
zero_responder.handle_requests_forever()

# In alternative to handle only one request and exit
# zero_responder.handle_request()
