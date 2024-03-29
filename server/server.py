import os

from sanic import Sanic
from sugar_api import CORS, Redis
from sugar_odm import MongoDB


CORS.set_origins('*')

server = Sanic('application-name')

@server.listener('before_server_start')
async def before_server_start(app, loop):
    MongoDB.set_event_loop(loop)
    await Redis.set_event_loop(loop)
    Redis.default_connection(host=os.getenv('REDIS_URI', 'redis://localhost'), minsize=os.getenv('REDIS_POOL_MIN', 5), maxsize=os.getenv('REDIS_POOL_MAX', 10))

@server.listener('before_server_stop')
async def before_server_stop(app, loop):
    MongoDB.close()
    await Redis.close()
