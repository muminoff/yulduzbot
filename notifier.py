import asyncio
import aiopg
import logging
from TwitterAPI import TwitterAPI
import base64
import os

dsn = 'dbname=yulduz user=yulduz password=yulduz host=127.0.0.1'
logger = logging.getLogger('asyncio')
logging.basicConfig(level=logging.DEBUG)


async def twitter_notify(conn):
    api = TwitterAPI(
        os.getenv('TWITTER_CONSUMER_KEY'),
        os.getenv('TWITTER_CONSUMER_SECRET'),
        os.getenv('TWITTER_ACCESS_TOKEN_KEY'),
        os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )

    async with conn.cursor() as cur:
        r = api.request('statuses/filter', {'track': 'putin'})

        for item in r:
            obj = item['text'] if 'text' in item else item['username']
            encoded_obj = base64.encodestring(obj.encode())
            print(encoded_obj)
            await cur.execute("NOTIFY twitter, '{}'".format(encoded_obj.decode()))


async def main():
    logger.debug("main")
    async with aiopg.create_pool(dsn) as pool:
        async with pool.acquire() as conn:
            twitter_notifier = twitter_notify(conn)
            await asyncio.gather(twitter_notifier)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
