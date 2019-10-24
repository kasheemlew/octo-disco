from typing import List, Dict


class FilterHandler:
    @classmethod
    def get_filter(cls, **params):
        filter_type = params.get('type')
        del params['type']
        if filter_type == 'xpath':
            return XpathFilter(**params)

    @classmethod
    def parse_handler(cls, filters_json: List[Dict[str, str]]):
        filters: List[GeneralFilter] = []
        for filter_json in filters_json:
            filter_obj = cls.get_filter(**filter_json)
            filters.append(filter_obj)
        return filters


class GeneralFilter:
    ...


class XpathFilter(GeneralFilter):
    def __init__(self, value, expression=None):
        self.value = value
        self.expression = expression

    def do_run(self):
        ...
