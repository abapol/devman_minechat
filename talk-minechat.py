import asyncio



async def write_chat():
    user = {
        "nickname": "Keen newuser",
        "account_hash": "bd24bee4-c11d-11ea-8c47-0242ac110002"
    }
    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5050)

    datar = await reader.readline()
    print(datar.decode())

    writer.write(user["account_hash"].encode())
    writer.write('\n'.encode())
    await writer.drain()

    writer.write('Hello!\n\n'.encode())
    await writer.drain()

    writer.close()


if __name__ == '__main__':
    asyncio.run(write_chat())