import aiofiles
import argparse
import asyncio
from datetime import datetime
from functools import partial


async def read_chat(parser_args):

    try:
        reader, writer = await asyncio.open_connection(parser_args.host, parser_args.port)

        while True:
            datetime_now = datetime.now().strftime("%Y.%m.%d %H:%M")

            data = await reader.readline()
            if not data:
                break

            async with aiofiles.open(parser_args.history, mode="a", encoding="utf-8") as outfile:
                await outfile.write(f'[{datetime_now}] {data.decode()}')
                outfile.close()
    finally:
        writer.close()
        await writer.wait_closed()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='minechat.dvmn.org', help="Host name")
    parser.add_argument('--port', type=int, default=5000, help="Port number")
    parser.add_argument('--history', type=str, default='minechat.history', help="Path to history file")
    read_chat = partial(read_chat, parser_args=parser.parse_args())

    asyncio.run(read_chat())
