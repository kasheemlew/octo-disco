import itertools
from typing import Any, Dict, List, Union

from lxml import etree


class ExprParser:
    @staticmethod
    def parse(expr: str, params: List[Dict[str, str]], this=None) -> List[Any]:
        result = []
        real_params = {}

        # Parse values
        for p in params:
            if p.get('type') == 'xpath':
                if not isinstance(this, etree._Element):
                    this = etree.HTML(this)
                eval_p = this.xpath(p.get('value'))
            else:
                eval_p = eval(p.get('value'))
                if hasattr(eval_p, '__iter__'):
                    eval_p = list(eval_p)
                if not isinstance(eval_p, list):
                    eval_p = [eval_p]
            real_params[p.get("key")] = eval_p

        param_keys = real_params.keys()
        param_product = itertools.product(*list(map(lambda x: real_params.get(x), param_keys)))

        # Generate result list
        for pp in param_product:
            formatted = expr.format(**dict(zip(param_keys, pp)))
            formatted_value = formatted
            try:
                formatted_value = eval(formatted_value)
            except SyntaxError:
                pass
            result.append(formatted_value)
        return result
