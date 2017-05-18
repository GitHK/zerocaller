# ZeroCaller

Is a zeroMQ implementation for RPC.

# RTC style operations

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



# Async operatons

Use the `ZeroSender` and a `ZeroReceiver` to issue asynchronous requests.

Check out the [examples folder](https://github.com/GitHK/zerocaller/tree/master/examples) for more details.


## Receiver

Define a callback that can be called by multiple senders.

    from zerocaller.zero_async import ZeroReceiver
    
    
    def say_hello(payload):
        print('Hello %s!' % payload)
    
    
    receiver = ZeroReceiver()
    receiver.register_handler('hello', say_hello)
    
    receiver.receive_action()


## Sender

Used to send a custom action mapped on the `receiver`.

    from zerocaller.zero_async import ZeroSender
    
    sender = ZeroSender()
    sender.send_action('hello', 'Zero the user!')
