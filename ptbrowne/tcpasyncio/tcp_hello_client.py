import asyncio

SERVERS = {
    'en': 8888,
    'fr': 8889
}

WHATSYOURNAME = {
    'en': 'What\'s your name ?',
    'fr': 'Quel est ton nom ?'
}

async def tcp_echo_client(language, name):
    loop = asyncio.get_event_loop()
    reader, writer = await asyncio.open_connection(
        '127.0.0.1',
        SERVERS[language],
        loop=loop
    )

    # print('Send: %r' % message)
    writer.write(name.encode())

    data = await reader.read()
    print('Received: %r' % data.decode())

    print('Close the socket')
    writer.close()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('language')
    args = parser.parse_args()
    message = input('{} '.format(WHATSYOURNAME[args.language]))
    asyncio.run(tcp_echo_client(args.language, message))

main()
