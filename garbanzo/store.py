import shortuuid
from loguru import logger
from motor import motor_asyncio

from garbanzo.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DB


class MongoStore:
    def __init__(self, db=None):
        db_name = MONGODB_DB or f'db_{shortuuid.ShortUUID().random(length=4)}'
        client = motor_asyncio.AsyncIOMotorClient(MONGODB_HOST, MONGODB_PORT)
        db = client[db_name]
        self.collection = db[db_name]

    async def store(self, **kwargs):
        logger.debug(f'started writing {kwargs}')
        result = await self.collection.insert_one(kwargs)
        logger.debug(f'finished with id {result.inserted_id}')
