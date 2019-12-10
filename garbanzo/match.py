from typing import List, Dict

from lxml import etree

from garbanzo.node import Node


class MatchHandler:
    @classmethod
    def get_match(cls, **params):
        match_type = params.get('type')
        del params['type']
        if match_type == 'xpath':
            return XpathMatch(**params)
        raise Exception('Unknown filter type')

    @classmethod
    def parse_match(cls, match_json: List[Dict[str, str]]):
        if not match_json:
            return []
        matches = []
        for jsn in match_json:
            obj = cls.get_match(**jsn)
            matches.append(obj)
        return matches


class XpathMatch:
    def __init__(self, value: str):
        self.value = value
        self.type = 'xpath'

    def do(self, elements: List[Node]):
        result = []
        for elem in elements:
            if not isinstance(elem, Node):
                elem = etree.HTML(elem)
            matched_elems = elem.xpath(self.value)
            # TODO
            if len(matched_elems) > 0:
                result.extend(elem.xpath(self.value))
        return result
