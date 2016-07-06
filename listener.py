import asyncio
import aiopg
import logging
from TwitterAPI import TwitterAPI
import json
import base64

dsn = 'dbname=yulduz user=yulduz password=yulduz host=127.0.0.1'
logger = logging.getLogger('asyncio')
logging.basicConfig(level=logging.DEBUG)


async def twitter_listen(conn):
    async with conn.cursor() as cur:
        await cur.execute("LISTEN twitter")
        while True:
            msg = await conn.notifies.get()
            msg = base64.decodestring(msg.payload.encode())
            logger.debug("Received <- {}".format(msg.decode()))


async def main():
    logger.debug("main")
    async with aiopg.create_pool(dsn) as pool:
        async with pool.acquire() as conn:
            twitter_listener = twitter_listen(conn)
            await asyncio.gather(twitter_listener)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
