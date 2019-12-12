from motor import motor_asyncio

from garbanzo.logger import logger


class MongoStore:
    def __init__(self, db='garbanzo_project'):
        client = motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        db = client[db]
        self.collection = db['garbanzo']

    async def store(self, **kwargs):
        logger.debug(f'started writing {kwargs}')
        result = await self.collection.insert_one(kwargs)
        logger.debug(f'finished with id {result.inserted_id}')
