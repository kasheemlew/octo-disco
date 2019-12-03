import asyncio
import itertools
import json
import os

from garbanzo.filter import FilterHandler
from garbanzo.match import MatchHandler
from garbanzo.source import SourceHandler
from garbanzo.job import Job
from garbanzo.utils.expression import ExprParser
from garbanzo.utils.logger import logger


class MainController:
    def __init__(self):
        self.inputq = asyncio.Queue()
        self.source_handler = SourceHandler()
        self.filter_handler = FilterHandler()
        self.match_handler = MatchHandler()

    def run(self):
        self.read_template()
        asyncio.run(self.run_parse_json())
        asyncio.run(self.run_jobs())

    def read_template(self):
        with open(os.path.join(os.path.dirname(__file__), 'template.json')) as json_file:
            data = json.load(json_file)
        self.inputq.put_nowait(data)

    async def run_parse_json(self):
        json_data = await self.inputq.get()

        assert 'source' in json_data.keys(), 'json_data has no sources'
        sources = self.source_handler.parse_source(json_data['source'])
        matches = self.match_handler.parse_match(json_data.get('match', []))
        filters = self.filter_handler.parse_filter(json_data.get('filter', []))
        name = json_data.get('name')
        host = json_data.get('host')
        targets = json_data.get('target', [])
        storage = json_data.get('store', [])

        await self.create_job('', name, host, sources, matches, filters, targets, storage)

    async def create_job(self, parent, name, host, sources, matches, filters, targets, storage):
        new_job = Job(parent, name, host, sources, matches, filters, targets, storage)
        await self.inputq.put(new_job)

    async def create_sub_job(self, job):
        for target in job.targets:
            user_defined_source = target.get('source')
            this = type('this', (), {
                'source': job.result,
                'host': target.get('host', job.host),
            })()
            if not user_defined_source:
                sources = job.result
            else:
                sources = []
                for source in user_defined_source:
                    if source.get('type') == 'expr':
                        sources.extend(ExprParser.parse(source['value'], source['param'], this))
                    else:
                        sources.append(source.get('value'))

            await self.create_job(
                parent=job.name,
                name=target.get('name', job.name + '1'),
                host=target.get('host', job.host),
                sources=sources,
                matches=self.match_handler.parse_match(target.get('match', [])),
                filters=self.filter_handler.parse_filter(target.get('filter', [])),
                targets=target.get('target', []),
                storage=target.get('store', [])
            )

    async def run_jobs(self):
        while True:
            try:
                job: Job = self.inputq.get_nowait()
                await job.run()
                await self.create_sub_job(job)
                logger.info(f"{job.name}: {job.result}; {job.storage}")
            except asyncio.QueueEmpty as e:
                break
