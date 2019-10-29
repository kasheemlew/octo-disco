import asyncio
import itertools
import json
import os

from src.handlers.filter import FilterHandler
from src.handlers.source import SourceHandler
from src.job import Job


class MainController:
    def __init__(self):
        self.inputq = asyncio.Queue()
        self.source_handler = SourceHandler()
        self.filter_handler = FilterHandler()

    def run(self):
        self.read_template()
        asyncio.run(self.run_parse_json())
        asyncio.run(self.run_job())

    def read_template(self):
        with open(os.path.join(os.path.dirname(__file__), 'template.json')) as json_file:
            data = json.load(json_file)
        self.inputq.put_nowait(data)

    async def run_parse_json(self):
        json_data = await self.inputq.get()

        assert 'sources' in json_data.keys(), 'json_data has no sources'
        sources = self.source_handler.parse_source(json_data.get('sources'))
        filters = self.filter_handler.parse_filter(json_data.get('filters', None))
        name = json_data.get('name')
        host = json_data.get('host')
        targets = json_data.get('targets', None)
        storage = json_data.get('storage', None)

        await self.create_job(name, host, sources, filters, targets, storage)

    async def create_job(self, name, host, sources, filters, targets, storage):
        new_job = Job(name, host, sources, filters, targets, storage)
        await self.inputq.put(new_job)

    async def create_sub_job(self, job):
        for target in job.get_targets():
            this = type('this', (), {
                'source': job.get_result(),
                'sources': target.get('sources', None),
                'host': target.get('host', job.host),
            })
            if this.sources is None:
                sources = job.get_result()
            else:
                sources = []
                for source in this.sources:
                    if source.get('type') == 'expression':
                        real_params = {}
                        for p in source.get('params'):
                            eval_p = eval(p.get('value'))
                            if not isinstance(eval_p, list):
                                eval_p = [eval_p]
                            real_params[p.get("key")] = eval_p
                        param_keys = list(real_params.keys())
                        param_product = itertools.product(*list(map(lambda x: real_params.get(x), param_keys)))
                        for pp in param_product:
                            sources.append(eval(source.get('value').format(**dict(zip(param_keys, pp)))))
                    else:
                        sources.append(source.get('value'))

            await self.create_job(
                name=target.get('name', job.name + '1'),
                host=target.get('host', job.host),
                sources=sources,
                filters=self.filter_handler.parse_filter(target.get('filters', None)),
                targets=target.get('targets', None),
                storage=target.get('storage', None)
            )

    async def run_job(self):
        while True:
            try:
                job: Job = self.inputq.get_nowait()
                print(
                    f'======{job.name}\n'
                    f'sources: {job.sources}\n'
                    f'filters: {job.filters}\n'
                    f'targets: {job.targets}\n'
                      )
                await job.run()
                result = job.get_result()
                targets = job.get_targets()
                if targets is not None:
                    await self.create_sub_job(job)
            except asyncio.QueueEmpty as e:
                print(e)
                break
