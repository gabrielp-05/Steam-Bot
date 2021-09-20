import asyncio

async def load_thread(fetchMessage):
    msg = '`Fetching data from Steam servers'
    await fetchMessage.edit(content=msg+'.`')
    await asyncio.sleep(0.5)
    await fetchMessage.edit(content=msg+'..`')
    await asyncio.sleep(0.5)
    await fetchMessage.edit(content=msg+'...`')
    await asyncio.sleep(0.5)
