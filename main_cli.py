import asyncio


async def read_chat(host, port):
    reader, writer = await asyncio.open_connection(host, port)

    while True:
        data = await reader.readline()
        if not data:
            break
        print(data.decode(), end='')


if __name__ == '__main__':
    host = 'minechat.dvmn.org'
    port = 5000
    asyncio.run(read_chat(host, port))
