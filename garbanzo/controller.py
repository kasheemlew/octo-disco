import asyncio
import json
import os
from typing import Dict, Union

from garbanzo.filter import FilterHandler
from garbanzo.job import Job
from garbanzo.logger import logger
from garbanzo.match import MatchHandler
from garbanzo.source import SourceHandler
from garbanzo.this import This
from garbanzo.utils.expression import ExprParser


class MainController:
    def __init__(self):
        self.source_handler = SourceHandler()
        self.filter_handler = FilterHandler()
        self.match_handler = MatchHandler()

    @staticmethod
    async def default_req_data() -> Dict[str, Union[str, Dict]]:
        with open(os.path.join(os.path.dirname(__file__), 'template.json')) as json_file:
            data = json.load(json_file)
        return data

    async def run(self, data: Dict[str, Union[str, Dict]] = None) -> None:
        self.inputq = asyncio.Queue()
        if data is None:
            data = await self.default_req_data()
        await self.create_init_task(data)
        t = asyncio.create_task(self.run_jobs())
        await self.inputq.join()
        t.cancel()

    async def create_init_task(self, json_data: Dict[str, Union[str, Dict]]) -> None:
        assert 'source' in json_data.keys(), 'json_data has no sources'
        sources = self.source_handler.parse_source(json_data['source'])
        matches = self.match_handler.parse_match(json_data.get('match', []))
        filters = self.filter_handler.parse_filter(json_data.get('filter', []))
        name = json_data.get('name')
        host = json_data.get('host')
        targets = json_data.get('target', [])
        storage = json_data.get('store', [])
        for source in sources:
            await self.create_job('', name, host, [source], matches, filters, targets, storage)

    async def create_job(self, *args, **kwargs):
        job = Job(*args, **kwargs)
        await self.inputq.put(job)

    async def create_sub_job(self, job: Job) -> None:
        logger.info(f"Create sub job for {job.name}: {job.result}; {job.storage}")
        for target in job.targets:
            user_defined_source = target.get('source')
            this = This(source=job.result, host=target.get('host', job.host))
            if not user_defined_source:
                sources = job.result
            else:
                sources = []
                for source in user_defined_source:
                    if source.get('type') == 'expr':
                        sources.extend(ExprParser.parse(source['value'], source['param'], this))
                    else:
                        sources.append(source.get('value'))
            for source in sources:
                await self.create_job(
                    parent=job,
                    name=target.get('name'),
                    host=target.get('host', job.host),
                    sources=[source],
                    matches=self.match_handler.parse_match(target.get('match', [])),
                    filters=self.filter_handler.parse_filter(target.get('filter', [])),
                    targets=target.get('target', []),
                    storage=target.get('store', [])
                )

    async def run_jobs(self):
        while True:
            job: Job = await self.inputq.get()
            await job.run()
            await self.create_sub_job(job)
            self.inputq.task_done()
            logger.info(f"{job.name}: {job.result}; {job.storage}")
