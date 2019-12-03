from unittest import TestCase

from garbanzo.utils.expression import ExprParser


class TestPythonParser(TestCase):
    def test_parse(self):
        self.assertEqual(
            ExprParser.parse('True', []),
            [True]
        )
        self.assertEqual(
            ExprParser.parse('{range}', [{'key': 'range', 'value': 'range(1,3)'}]),
            [1, 2]
        )
        self.assertEqual(
            ExprParser.parse('"prefix/"+"{range}"', [{'key': 'range', 'value': 'range(1,3)'}]),
            ['prefix/1', 'prefix/2']
        )
        self.assertEqual(
            ExprParser.parse(
                "https://n.netease.com/forum-74-{range}.html",
                [{"key": "range", "value": "range(1,3)"}]
            ),
            ["https://n.netease.com/forum-74-1.html", "https://n.netease.com/forum-74-2.html"],
        )
