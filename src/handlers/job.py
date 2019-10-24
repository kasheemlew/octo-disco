class JobHandler:
    def __init__(self, in_chan, out_chan):
        self.in_chan = in_chan
        self.out_chan = out_chan

    @staticmethod
    def parse(job_declaration):
        job_attrs = {
            'name': '',
            'host': '',
            'sources': [],
            'filters': [],
            'targets': [],
            'storage': None,
        }

        assert type(job_declaration) == dict, 'Job declaration not of type Dict!'
        for k in job_declaration.keys():
            assert k in job_attrs.keys() and type(k) == job_attrs.get(k)

        job_attrs['name'] = job_declaration.get('name')
        job_attrs['host'] = job_declaration.get('host')
        job_attrs['filters'] = job_declaration.get('filters')
        job_attrs['targets'] = job_declaration.get('targets')
        job_attrs['storage'] = job_declaration.get('storage')

        return job_attrs

    async def load_job(self):
        job_declaration = await self.in_chan.get()
        job_attrs = self.parse(job_declaration)
        await self.out_chan.put(job_attrs)
