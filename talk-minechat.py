import asyncio
import logging
import json

'''
    user = {
        "nickname": "Keen newuser",
        "account_hash": "bd24bee4-c11d-11ea-8c47-0242ac110002"
    }
    
'''



async def reader_data(reader):
    dataread = await reader.readline()
    logging.debug(dataread.decode())
    return dataread.decode()

async def writer_data(writer, message):
    datawrite = message + '\n'
    writer.write(datawrite.encode())
    await writer.drain()
    logging.debug(datawrite)


async def get_token():

    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5050)

    message = input(await reader_data(reader))
    await writer_data(writer, message)

    readdata = await reader_data(reader)
    if message:
        user = json.loads(readdata)
        if user is None:
            print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        else:
            print('Вы вошли')
            return user

    await writer_data(writer, input('Введите новое имя пользователя'))
    return json.loads(await reader_data(reader))




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(get_token())