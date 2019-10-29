from abc import ABC, abstractmethod
from typing import List, Dict

from lxml import etree


class FilterHandler:
    """
    Filter types: expression, xpath
    """
    @classmethod
    def get_filter(cls, **params):
        filter_type = params.get('type')
        del params['type']
        if filter_type == 'xpath':
            return XpathFilter(**params)
        elif filter_type == 'expression':
            return ExpressionFilter(**params)
        raise Exception('Unknown filter type')

    @classmethod
    def parse_filter(cls, filters_json: List[Dict[str, str]]):
        if filters_json is None or len(filters_json) == 0:
            return None
        filters: List[GeneralFilter] = []
        for filter_json in filters_json:
            filter_obj = cls.get_filter(**filter_json)
            filters.append(filter_obj)
        return filters


class GeneralFilter(ABC):
    @abstractmethod
    def do(self, elements: List[etree._Element]): ...


class XpathFilter(GeneralFilter):
    def __init__(self, value: str):
        self.value = value
        self.type = 'xpath'

    def do(self, elements: List[etree._Element]):
        result = []
        for elem in elements:
            print(elem)
            filtered_elems = elem.xpath(self.value)
            if len(filtered_elems) > 0:
                result.extend(elem.xpath(self.value))
        return result


class ExpressionFilter(GeneralFilter):
    def __init__(self, value: str, params: List[Dict[str, str]]):
        self.value = value
        self.type = 'expression'
        self.params = params

    def do(self, source: List[etree._Element]):
        result = []
        for elem in source:
            real_params = {}
            for param in self.params:
                p_type = param.get('type')
                if p_type == 'xpath':
                    p_values = elem.xpath(param.get('value'))
                    if len(p_values) == 0:
                        p_value = None
                    else:
                        p_value = p_values[0]
                    real_params[param.get('key')] = p_value
                elif type == 'python':
                    real_params[param.get('key')] = eval(param.get('value', None))
            try:
                if eval(self.value.format(**real_params)):
                    result.append(elem)
            except:
                pass
        return result
