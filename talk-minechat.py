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



async def register(reader, writer):

    message = input(await reader_data(reader))
    await writer_data(writer, message)

    readdata = await reader_data(reader)
    if message:
        user = json.loads(readdata)
        if user is None:
            print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
            return None
        else:
            print('Вы вошли')
            return user

    await writer_data(writer, input(readdata).replace(r'\n',''))
    return json.loads(await reader_data(reader))


async def authorise(reader, writer, user):
    await reader_data(reader)
    await writer_data(writer, user["account_hash"])
    readdata = await reader_data(reader)


async def submit_message(writer):
    while True:
        message = input().replace(r'\n','')
        await writer_data(writer, message)
        if message.lower() == 'bye':
            break

    
async def minechat():
    while True:
        reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5050)
        user = await register(reader, writer)
        writer.close()
        await writer.wait_closed()    
        if user:
            break

    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5050)        
    await authorise(reader, writer, user)
    await submit_message(writer)

    writer.close()
    await writer.wait_closed()    
        


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(minechat())