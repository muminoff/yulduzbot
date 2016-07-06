import asyncio
import aiopg
import logging
from TwitterAPI import TwitterAPI
import base64
import os
from urllib.parse import urlparse

postgres_url = os.getenv('DATABASE_URL', 'postgres://yulduz:yulduz@localhost:5432/yulduz')
postgres = urlparse(postgres_url)

dsn = """
dbname={db_name}
user={db_user}
password={db_password}
host={db_host}
port={db_port}
""".format(
    db_name=postgres.path[1:],
    db_user=postgres.username,
    db_password=postgres.password,
    db_host=postgres.hostname,
    db_port=postgres.port)

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
