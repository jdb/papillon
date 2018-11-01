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


server_configs = {
    'en': (greet('Hello'), '127.0.0.1', 8888),
    'fr': (greet('Bonjour'), '127.0.0.1', 8889)
}


def run_servers(loop, configs):
    servers = {}
    for lang, server_config in server_configs.items():
        server_coro = asyncio.start_server(*server_config)
        servers[lang] = loop.run_until_complete(server_coro)

    for lang, server in servers.items():
        print('Serving on {}'.format(server.sockets[0].getsockname()))

    return servers


def close_servers(loop, servers):
    for server in servers:
        server.close()
        loop.run_until_complete(server.wait_closed())


loop = asyncio.get_event_loop()

servers = run_servers(loop, server_configs)
# Serve requests until Ctrl+C is pressed
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
close_servers(loop, servers.values())
loop.close()
