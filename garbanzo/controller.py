import asyncio
import json
import os
from typing import Dict, Union, List

from loguru import logger

from garbanzo.filter import FilterHandler
from garbanzo.job import Job
from garbanzo.match import MatchHandler
from garbanzo.source import SourceHandler
from garbanzo.this import This
from garbanzo.utils.expression import ExprParser


class MainController:
    def __init__(self):
        self.task_count = 0
        self.task_done_count = 0
        self.inputq: asyncio.Queue
        self.source_handler = SourceHandler()
        self.filter_handler = FilterHandler()
        self.match_handler = MatchHandler()
        self.template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
        self.template_json = os.environ.get('GJF', 'steam.json')

    async def default_req_data(self) -> Dict[str, Union[List, Dict, str]]:
        with open(os.path.join(self.template_dir, self.template_json)) as json_file:
            data = json.load(json_file)
        return data

    async def run(self, data: Dict[str, Union[List, Dict, str]] = None):
        self.inputq = asyncio.Queue()
        if data is None:
            data = await self.default_req_data()
        await self.create_init_task(data)
        t = asyncio.create_task(self.run_jobs())

        await self.inputq.join()
        logger.info(f'task count: {self.task_count}, task_done_count: {self.task_done_count}')
        t.cancel()

    async def create_init_task(self, json_data: Dict[str, Union[List, Dict, str]]):
        assert 'source' in json_data.keys(), 'json_data has no source'
        cookies = json_data.get('cookies', {})
        timeout = json_data.get('timeout', 60)

        sources = self.source_handler.parse_source(json_data['source'])
        matches = self.match_handler.parse_match(json_data.get('match', []))
        filters = self.filter_handler.parse_filter(json_data.get('filter', []))
        name = json_data.get('name')
        host = json_data.get('host')
        targets = json_data.get('target', [])
        storage = json_data.get('store', [])
        for source in sources:
            await self.create_job('', name, host, [source], cookies, timeout, matches, filters, targets, storage)

    async def create_job(self, *args, **kwargs):
        self.task_count += 1
        job = Job(*args, **kwargs)
        await self.inputq.put(job)

    async def create_sub_job(self, job: Job):
        logger.debug(f"Create sub job for {job.name}: {job.result}; {job.storage}")
        for target in job.targets:
            user_defined_source = target.get('source')
            this = This(
                source=job.result, 
                host=target.get('host', job.host),
                parent=job,
            )
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
                    cookies=target.get('cookies', job.cookies),
                    timeout=target.get('timeout', job.timeout),
                    sources=[source],
                    matches=self.match_handler.parse_match(target.get('match', [])),
                    filters=self.filter_handler.parse_filter(target.get('filter', [])),
                    targets=target.get('target', []),
                    storage=target.get('store', [])
                )
    
    async def create_job_task(self, job):
        try:
            await job.run()
            await self.create_sub_job(job)
        except Exception as e:
            logger.warning(f"Job {job.to_json()} failed: {e}")
        finally:
            self.task_done_count += 1
            self.inputq.task_done()
        logger.debug(f"{job.name}: {job.result}; {job.storage}")

    async def run_jobs(self):
        while True:
            job: Job = await self.inputq.get()
            asyncio.create_task(self.create_job_task(job))

