from functools import partial
import argparse
import asyncio
import logging
import json


async def reader_data(reader):
    dataread = await reader.readline()
    logging.debug(dataread.decode())
    return dataread.decode()

async def writer_data(writer, message):
    datawrite = message + '\n'
    writer.write(datawrite.encode())
    await writer.drain()
    logging.debug(datawrite)


async def authenticate(reader, writer, nickname):
    await writer_data(writer, nickname)
    return json.loads(await reader_data(reader))


async def register(reader, writer, token, nickname):

    await reader_data(reader)
    await writer_data(writer, token)

    readdata = await reader_data(reader)
    if not token:    
        await authenticate(reader, writer, nickname.replace(r'\n',''))
        return
    
    user = json.loads(readdata)
    if user is None:
        print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
    return user
  

async def authorise(reader, writer, user):
    await reader_data(reader)
    await writer_data(writer, user["account_hash"])
    readdata = await reader_data(reader)


async def submit_message(writer, message):    
    await writer_data(writer, message.replace(r'\n','')+'\n')        

    
async def minechat(parser_args):
    
    try:
        reader, writer = await asyncio.open_connection(parser_args.host, parser_args.port)
        user = await register(reader, writer, parser_args.token, parser_args.nickname)
        writer.close()
        await writer.wait_closed()    
        if not user:
            return

        reader, writer = await asyncio.open_connection(parser_args.host, parser_args.port)        
        await authorise(reader, writer, user)
        await submit_message(writer, parser_args.message)
    finally:
        writer.close()
        await writer.wait_closed()    
        

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='minechat.dvmn.org', help="Host name")
    parser.add_argument('--port', type=int, default=5050, help="Port number")
    parser.add_argument('--token', type=str, default='', help="Enter your token")
    parser.add_argument('--message', type=str, default='Hello', help="Enter your massage")
    parser.add_argument('--nickname', type=str, default='Zina', help="Your name")
    
    minechat = partial(minechat, parser_args=parser.parse_args())

    asyncio.run(minechat())