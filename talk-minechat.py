import asyncio
import logging
import json


async def readerData(reader):
    dataread = await reader.readline()
    logging.debug(dataread.decode())
    return dataread.decode()

async def writerData(writer, message):
    datawrite = message + '\n'
    writer.write(datawrite.encode())
    await writer.drain()
    logging.debug(datawrite)


async def write_chat():
    user = {
        "nickname": "Keen newuser",
        "account_hash": "bd24bee4-c11d-11ea-8c47-0242ac110002"
    }
    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5050)

    await writerData(writer, input(await readerData(reader)))

    if json.loads(await readerData(reader)) is None:
        await writerData(writer, input('Неизвестный токен. Проверьте его или зарегистрируйте заново.'))







'''
    dataread = await reader.readline()
    if dataread:
        logging.debug(dataread.decode())

    message = input('Введите токен для входа: ')

    datawrite = message + '\n'
    writer.write(datawrite.encode())
    await writer.drain()
    logging.debug(datawrite)

    dataread = await reader.readline()
    if dataread:
        logging.debug(dataread.decode())
        
    if json.loads(dataread.decode()) is None:
        print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
'''
    # assert json.loads(dataread.decode()) is not None, 'Неизвестный токен. Проверьте его или зарегистрируйте заново.'




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(write_chat())