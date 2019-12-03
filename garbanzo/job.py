from typing import List, Dict

from lxml import etree
import asyncio
import aiohttp

from garbanzo.filter import GeneralFilter
from garbanzo.match import XpathMatch
from garbanzo.store import MongoStore


class Job:
    def __init__(
            self,
            parent: str,
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

    async def run(self):
        await self.parse_source()
        self.match_source()
        self.filter_source()
        self.store()

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
        result = self.source
        for m in self.matches:
            result = m.do(result)
        self.result = result

    def filter_source(self):
        result = self.result
        for f in self.filters:
            result = f.do(result)
        self.result = result

    def store(self):
        if not self.storage:
            return
        for r in self.result:
            MongoStore().store(**{
                'parent': self.parent,
                'name': self.name,
                self.storage.get('field', 'default_field'): r
            })
