from zerocaller import ZeroAwaiter


def say_hello_handler(payload):
    return "Hello %s!" % payload


awaiter = ZeroAwaiter()
awaiter.register_handler('say_hello', say_hello_handler)
awaiter.handle_requests_forever()

# In alternative to handle only one request and exit
# awaiter.handle_request()
