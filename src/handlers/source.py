from copy import copy
from typing import List


class SourceHandler:
    @classmethod
    def get_source(cls, **params):
        source_type = params.get('type')
        del params['type']
        if source_type == 'expression':
            return ExpressionSource(**params)
        return NormalSource(params)

    @classmethod
    def parse_source(cls, sources):
        results = []
        for source_json in sources:
            source = cls.get_source(**source_json)
            source.parse()
            results.extend(source.get_vals())
        return results


class GeneralSource:
    def parse(self): ...
    def get_vals(self) -> List[str]: ...


class ExpressionSource(GeneralSource):
    def __init__(self, value, params):
        self.params = params
        self.source_template = value
        self.results = []

    def parse(self):
        for p in self.params:
            p_value = p.get('value')
            if p.get('type') == 'python':
                p_value = eval(p_value)

            if type(p_value) == range:
                p_value = list(p_value)
            if type(p_value) != list:
                p_value = [p_value]
            for i in p_value:
                self.replace(p.get('key'), i)

    def replace(self, k, v):
        s = copy(self.source_template)
        self.results.append(s.replace(f'{{{k}}}', str(v)))

    def get_vals(self):
        return self.results


class NormalSource(GeneralSource):
    def __init__(self, value, *args, **kwargs):
        self.source = value

    def get_vals(self):
        return [self.source]
