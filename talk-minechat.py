from functools import partial
import argparse
import asyncio
import logging
import json


class UnknownTokenError(Exception):
	pass


async def get_reader_data(reader):
    data = await reader.readline()
    logging.debug(data.decode())
    return data.decode()

async def get_writer_data(writer, message):
    data = message + '\n'
    writer.write(data.encode())
    await writer.drain()
    logging.debug(data)


async def authenticate(reader, writer, nickname):
    await get_writer_data(writer, nickname)
    return json.loads(await get_reader_data(reader))


async def register(reader, writer, token, nickname):

    await get_reader_data(reader)
    await get_writer_data(writer, token)

    data = await get_reader_data(reader)
    if not token:    
        await authenticate(reader, writer, nickname.replace(r'\n',''))
        return
    
    user = json.loads(data)
    if user is None:
        raise UnknownTokenError
    return user
  

async def authorise(reader, writer, user):
    await get_reader_data(reader)
    await get_writer_data(writer, user["account_hash"])
    data = await get_reader_data(reader)


async def submit_message(writer, message):    
    await get_writer_data(writer, message.replace(r'\n','')+'\n')        

    
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

    try:
        asyncio.run(minechat())
    except UnknownTokenError:
    	print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')