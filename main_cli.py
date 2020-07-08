import asyncio
import aiofiles
from datetime import datetime



async def read_chat(host, port, history_file):
    reader, writer = await asyncio.open_connection(host, port)

    while True:
        datetime_now = datetime.now().strftime("%Y.%m.%d %H:%M")

        data = await reader.readline()
        if not data:
            break

        async with aiofiles.open(history_file, mode="a", encoding="utf-8") as outfile:
            await outfile.write(f'[{datetime_now}] {data.decode()}')
            outfile.close()


if __name__ == '__main__':
    host = 'minechat.dvmn.org'
    port = 5000
    history_file = 'minechat.history'
    asyncio.run(read_chat(host, port, history_file))
