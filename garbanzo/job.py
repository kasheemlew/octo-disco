import asyncio
from typing import List, Dict, Generator, Any

import aiohttp
import shortuuid
from loguru import logger
from lxml import etree

from garbanzo.filter import GeneralFilter
from garbanzo.match import XpathMatch
from garbanzo.store import MongoStore


class Job:
    def __init__(
            self,
            parent: 'Job',
            name: str,
            host: str,
            sources: str,
            cookies: Dict[str, str],
            timeout: int,
            matches: List[XpathMatch],
            filters: List[GeneralFilter],
            targets: List[Dict],
            storage: Dict
    ):
        self.parent = parent
        self.name = name
        self.host = host
        self.cookies = cookies
        self.timeout = timeout
        self.sources = sources
        self.matches = matches
        self.filters = filters
        self.targets = targets
        self.storage = storage
        self.source: List[str] = []
        self.result = []
        self.uuid = shortuuid.ShortUUID().random(length=4)
        self.values: Dict[str, List] = {}

    def to_json(self):
        return {
            'name': self.name,
            'sources': self.sources,
        }

    async def run(self):
        await self.parse_source()
        logger.debug(self.source)
        self.match_source()
        self.filter_source()
        await self.store()
        logger.debug(f'Job {self.name}@{self.uuid} finished')

    @staticmethod
    async def fetch(session, data):
        c = data
        if isinstance(data, str) and data.startswith(('http', 'https')):
            try:
                async with session.get(
                    data, proxy='http://localhost:8080', ssl=False,
                ) as resp:
                    c = etree.HTML(await resp.text())
            except Exception:
                c = etree.HTML('')
        if c is not None:
            return c

    async def parse_source(self):
        datas = self.sources
        timeout = aiohttp.ClientTimeout(self.timeout)
        async with aiohttp.ClientSession(cookies=self.cookies, timeout=timeout) as session:
            tasks = [self.fetch(session, data) for data in datas]
            self.source.extend(await asyncio.gather(*tasks))
            logger.debug(f'{self.name}@{self.uuid} get source: {self.source}')

    def match_source(self):
        logger.debug(f'{self.name}@{self.uuid} started matching: {self.source}')
        for m in self.matches:
            match_name, result = m.do(self.source, self)
            if result:
                self.result.extend(result)
            if match_name is not None:
                self.values[match_name] = result
        logger.debug(f'{self.name}@{self.uuid} finished matching: {self.result}')

    def filter_source(self):
        logger.debug(f'{self.name}@{self.uuid} started filtering')
        result = self.result
        for f in self.filters:
            result = f.do(result)
        self.result = result
        logger.debug(f'{self.name}@{self.uuid} finished filtering')

    def find_ancestors_uuid(self) -> Generator[Any, str, Any]:
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
        document = {
            'parent': '-'.join(self.find_ancestors_uuid()),
            'name': self.name,
            'uuid': self.uuid,
        }
        for store_item in self.storage:
            store_value = self.values.get(store_item['name'])
            if isinstance(store_value, list):
                store_value.append('')
                store_value = store_value[0]
            document[store_item['field']] = store_value
        await MongoStore().store(**document)
