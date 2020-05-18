from typing import List, Dict, Union

from lxml import etree

from garbanzo.node import Node
from garbanzo.utils.expression import ExprParser


class MatchBuilder:
    def __init__(self, params):
        self.job = params.get('job')
        self.name = params.get('name', '')
        self.value = params.get('value', '')
        self.join = params.get('join', False)
        self.joiner = params.get('joiner', ' ')
        self.index = params.get('index', -1)
        self.ttype = params.get('type')
        self.params = params.get('param')

    def build(self):
        return {
            'job': self.job,
            'name': self.name,
            'value': self.value,
            'join': self.join,
            'joiner': self.joiner,
            'index': self.index,
            'param': self.params,
        }


class MatchHandler:
    @classmethod
    def get_match(cls, **params):
        builder = MatchBuilder(params)
        if builder.ttype == 'xpath':
            return XpathMatch(builder)
        if builder.ttype == 'expr':
            return ExprMatch(builder)
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


class GeneralMatch:...


class XpathMatch(GeneralMatch):
    def __init__(self, builder: MatchBuilder):
        self.type = 'xpath'

        params = builder.build()
        self.name = params['name']
        self.value = params['value']
        self.join = params['join']
        self.joiner = params['joiner']
        self.index = params['index']

    def do(self, elements: List[Union[Node, str]], *args, **kwargs):
        result = []
        for elem in elements:
            if elem is None or len(elem) == 0:
                continue
            if not isinstance(elem, Node):
                elem = etree.HTML(elem)
            for e in elem.xpath(self.value):
                if isinstance(e, str):
                    ev = e.strip()
                    if len(ev) > 0:
                        result.append(ev)
                elif e is not None:
                    result.append(e)
        if self.join:
            result = [self.joiner.join(result)]
        elif 0 <= self.index < len(result):
            result = [result[self.index]]
        return self.name, result

    def to_json(self):
        return {
            'name': self.name,
            'value': self.value,
            'type': self.type,
            'join': self.join,
            'joiner': self.joiner,
            'index': self.index,
        }


class ExprMatch(GeneralMatch):
    def __init__(self, builder: MatchBuilder):
        self.type = 'expr'

        params = builder.build()
        self.name = params['name']
        self.value = params['value']
        self.join = params['join']
        self.joiner = params['joiner']
        self.index = params['index']
        self.params = params['param']
    
    def do(self, elements: List[Union[Node, str]], job):
        return self.name, ExprParser.parse(self.value, self.params, job)