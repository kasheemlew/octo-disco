from unittest import TestCase

from src.handlers.source import ExpressionSource


class TestExpressionSource(TestCase):
    def setUp(self):
        self.expr = ExpressionSource(
            value="https://n.netease.com/forum-74-{range}.html",
            params=[{"key": "range", "value": "range(1,4)"}]
        )
        self.result = [
            "https://n.netease.com/forum-74-1.html",
            "https://n.netease.com/forum-74-2.html",
            "https://n.netease.com/forum-74-3.html",
        ]

    def test_parse(self):
        self.expr.parse()
        self.assertEqual(self.expr.get_vals(), self.result)
