import asyncio


def greet(greeting):
    async def wrapped(reader, writer):
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        # print("Received %r from %r" % (message, addr))

        print("Send: %r" % message)
        writer.write('{} {} !'.format(greeting, data.decode()).encode())
        await writer.drain()

        print("Close the client socket")
        writer.close()
    return wrapped

loop = asyncio.get_event_loop()
coro = asyncio.start_server(greet('Hello'), '127.0.0.1', 8888, loop=loop)
coro2 = asyncio.start_server(greet('Bonjour'), '127.0.0.1', 8889, loop=loop)
server = loop.run_until_complete(coro)
server2 = loop.run_until_complete(coro2)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
