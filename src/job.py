from typing import List, Dict

from lxml import etree
import asyncio
import aiohttp

from src.handlers.filter import GeneralFilter


class Job:
    def __init__(
            self,
            name: str,
            host: str,
            sources: str,
            filters: List[GeneralFilter],
            targets: List[Dict],
            storage: Dict
    ):
        self.name = name
        self.host = host
        self.sources = sources
        self.filters = filters
        self.targets = targets
        self.storage = storage
        self.__result = None

    async def run(self):
        await self.__parse_source()
        self.__filter_source()

    @staticmethod
    async def fetch(session, data):
        c = data
        if isinstance(data, str) and data.startswith(('http', 'https')):
            async with session.get(data) as resp:
                c = etree.HTML(await resp.text())
        if c is not None:
            return c

    async def __parse_source(self):
        datas = self.sources
        self.__source = []

        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, data) for data in datas]
            self.__source.extend(await asyncio.gather(*tasks))

    def __filter_source(self):
        result = self.__source
        if self.filters is not None and len(self.filters) > 0:
            for f in self.filters:
                result = f.do(result)
                print(result)
        self.__result = result

    def get_result(self):
        return self.__result

    def get_targets(self):
        return self.targets
