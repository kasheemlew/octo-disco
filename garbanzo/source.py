from abc import ABC, abstractmethod
from typing import List

from garbanzo.utils.expression import ExprParser


class SourceHandler:
    @classmethod
    def get_source(cls, **params):
        source_type = params.get('type')
        del params['type']
        if source_type == 'expr':
            return ExpressionSource(**params)
        return NormalSource(**params)

    @classmethod
    def parse_source(cls, sources):
        results = []
        for source_json in sources:
            source = cls.get_source(**source_json)
            source.parse()
            results.extend(source.vals())
        return results


class GeneralSource(ABC):
    @abstractmethod
    def parse(self): ...

    @abstractmethod
    def vals(self) -> List[str]: ...


class ExpressionSource(GeneralSource):
    def __init__(self, value, param):
        self.params = param
        self.source_template = value
        self.results = []

    def parse(self):
        self.results.extend(ExprParser.parse(self.source_template, self.params))

    def vals(self):
        return self.results


class NormalSource(GeneralSource):
    def __init__(self, value):
        self.results = []
        self.source = value

    def parse(self):
        self.results.append(self.source)

    def vals(self):
        return self.results
