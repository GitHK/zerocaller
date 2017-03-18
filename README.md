# ZeroCaller

Is a zeroMQ implementation for RPC.

# Usage

Use the `ZeroAwaiter` and a `ZeroRequester` to await for commands and issue requests.
 
Check out the [examples folder](https://github.com/GitHK/zerocaller/tree/master/examples) for more details.

## Awaiter

Initialize and register the `say_hello_handler`. It will always receive and argument called `payload`containing 
pickled objects.

    from zerocaller import ZeroAwaiter

    def say_hello_handler(payload):
        return "Hello %s!" % payload
    
    
    awaiter = ZeroAwaiter()
    awaiter.register_handler('say_hello', say_hello_handler)
    awaiter.handle_requests_forever()
    
    # In alternative to handle only one request and exit
    # awaiter.handle_request()


## Requester

In order to issue a call to the `say_hello_handler` in the awaiter call the `execute_remotely`functon 
with the name provided at registration time and a picklable object as a payload.

    from zerocaller import ZeroRequester
    
    requester = ZeroRequester()
    result = requester.execute_remotely('say_hello', 'world')
    
    print(result)



