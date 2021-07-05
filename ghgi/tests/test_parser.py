#!/usr/bin/env python
from unittest import TestCase
from ghgi.parser import amounts


PARSER_SAMPLE = [
    ('1 cup flour', {
        'qtys':[{'unit': 'cup', 'qty': 1.0}],
        'names': ['flour'],
        'mods': [],
    }),
    ('1 c flour', {
        'qtys':[{'unit': 'cup', 'qty': 1.0}],
        'names': ['flour'],
        'mods': [],
    }),
    ('1.5c flour', {
        'qtys':[{'unit': 'cup', 'qty': 1.5}],
        'names': ['flour'],
        'mods': [],
    }),
    ('1 1/2c flour', {
        'qtys':[{'unit': 'cup', 'qty': 1.5}],
        'names': ['flour'],
        'mods': [],
    }),
    ('yada yada', {
        'qtys':[{'unit': 'ea', 'qty': 1}],
        'names': ['yada yada'],
        'mods': [],
    }),
    ('chopped yada yada', {
        'qtys':[{'unit': 'ea', 'qty': 1}],
        'names': ['yada yada'],
        'mods': ['chopped'],
    }),
]


class TestParser(TestCase):

    def test_labels(self):
        for sample in PARSER_SAMPLE:
            self.assertEqual(amounts(sample[0]), sample[1])


