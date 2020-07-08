import asyncio
import logging


async def write_chat():
    user = {
        "nickname": "Keen newuser",
        "account_hash": "bd24bee4-c11d-11ea-8c47-0242ac110002"
    }
    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5050)

    dataread = await reader.readline()
    if dataread:
        logging.debug(f'sender:{dataread.decode()}')

    datawrite = user["account_hash"]+'\n'
    writer.write(datawrite.encode())
    await writer.drain()
    logging.debug(f'writer:{datawrite}')

    writer.write('Hello!\n\n'.encode())
    await writer.drain()

    writer.close()


if __name__ == '__main__':
    asyncio.run(write_chat())