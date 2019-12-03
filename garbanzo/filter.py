from abc import ABC, abstractmethod
from typing import List, Dict

from lxml import etree

from garbanzo.utils.expression import ExprParser


class FilterHandler:
    """
    Filter types: expression, xpath
    """
    @classmethod
    def get_filter(cls, **params):
        filter_type = params.get('type')
        del params['type']
        if filter_type == 'expr':
            return ExpressionFilter(**params)
        raise Exception('Unknown filter type')

    @classmethod
    def parse_filter(cls, filters_json: List[Dict[str, str]]):
        if not filters_json:
            return []
        filters: List[GeneralFilter] = []
        for filter_json in filters_json:
            filter_obj = cls.get_filter(**filter_json)
            filters.append(filter_obj)
        return filters


class GeneralFilter(ABC):
    @abstractmethod
    def do(self, elements: List[etree._Element]): ...


class ExpressionFilter(GeneralFilter):
    def __init__(self, value: str, param: List[Dict[str, str]]):
        self.value = value
        self.type = 'expr'
        self.params = param

    def do(self, source: List[etree._Element]):
        result = []
        for elem in source:
            if all(ExprParser.parse(self.value, self.params, elem)):
                result.append(elem)
        return result
