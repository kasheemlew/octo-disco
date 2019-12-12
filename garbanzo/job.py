import asyncio
from typing import List, Dict

import aiohttp
import shortuuid
from lxml import etree

from garbanzo.filter import GeneralFilter
from garbanzo.logger import logger
from garbanzo.match import XpathMatch
from garbanzo.store import MongoStore


class Job:
    def __init__(
            self,
            parent: 'Job',
            name: str,
            host: str,
            sources: str,
            matches: List[XpathMatch],
            filters: List[GeneralFilter],
            targets: List[Dict],
            storage: Dict
    ):
        self.parent = parent
        self.name = name
        self.host = host
        self.sources = sources
        self.matches = matches
        self.filters = filters
        self.targets = targets
        self.storage = storage
        self.source = []
        self.result = None
        self.uuid = shortuuid.ShortUUID().random(length=4)

    async def run(self):
        await self.parse_source()
        self.match_source()
        self.filter_source()
        await self.store()
        logger.debug(f'Job {self.name}@{self.uuid} finished')

    @staticmethod
    async def fetch(session, data):
        c = data
        if isinstance(data, str) and data.startswith(('http', 'https')):
            async with session.get(data) as resp:
                c = etree.HTML(await resp.text())
        if c is not None:
            return c

    async def parse_source(self):
        datas = self.sources
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, data) for data in datas]
            self.source.extend(await asyncio.gather(*tasks))

    def match_source(self):
        logger.debug(f'{self.name}@{self.uuid} started matching')
        result = self.source
        for m in self.matches:
            result = m.do(result)
        self.result = result
        logger.debug(f'{self.name}@{self.uuid} finished matching')

    def filter_source(self):
        logger.debug(f'{self.name}@{self.uuid} started filtering')
        result = self.result
        for f in self.filters:
            result = f.do(result)
        self.result = result
        logger.debug(f'{self.name}@{self.uuid} finished filtering')

    def find_ancestors_uuid(self) -> List[str]:
        logger.debug(f'in progress of find_ancestors_uuid, current {self.uuid}')
        p = self.parent
        while p:
            yield p.uuid
            p = p.parent

    async def store(self):
        if not self.storage:
            logger.debug(f'{self.name}@{self.uuid} has nothing to store')
            return
        logger.debug(f'{self.name}@{self.uuid} started storing')
        for r in self.result:
            if not r:
                continue
            await MongoStore().store(**{
                'parent': '-'.join(self.find_ancestors_uuid()),
                'name': self.name,
                'uuid': self.uuid,
                self.storage.get('field', 'default_field'): r
            })
        logger.debug(f'{self.name}@{self.uuid} finished storing')
