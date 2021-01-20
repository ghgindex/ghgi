from unittest import TestCase
import json
from io import StringIO
from ghgi.trigram import Trigram, build_indexes

class TestTrigram(TestCase):
    def test_trigrams(self):
        trigrams = [
            ('o', ['o']),
            ('on', ['on']),
            ('one', ['one']),
            ('onet', ['one', 'net']),
            ('one t', ['one', 'ne ', 'e t']),
            (' one t ', ['one', 'ne ', 'e t']),
            ('abc', ['abc']),
            ('ABc', ['abc']),
            (' abC ', ['abc']),
            ('abcdef', ['abc', 'bcd', 'cde', 'def']),
            ('abc DEF', ['abc', 'bc ', 'c d', ' de', 'def']),
        ]
        for seed, tris in trigrams:
            self.assertEqual(Trigram.trigrams(seed), tris)

    def test_file_loads(self):
        Trigram._product_index = None
        Trigram._aka_index = None
        self.assertNotEqual(Trigram.product_index(), None)
        self.assertNotEqual(Trigram.aka_index(), None)


    def test_indexes(self):
        products = {
            'test':{
                'names': [
                    'alpha',
                    'beta',
                    'theta'
                ]
            },
            'test2':{
                'names': [
                    'alpha2',
                    'theta2'
                ]
            }

        }
        f = StringIO(json.dumps(products))
        aka_index, trigram_product_index = build_indexes(f)
        # confirm all names present in index and point to the right product
        self.assertTrue(all([name in aka_index for name in ['test', 'test2']]))
        self.assertTrue(all([name in aka_index for name in products['test']['names']]))
        self.assertTrue(all([name in aka_index for name in products['test2']['names']]))
        self.assertTrue(all([v[0] in products for k,v in aka_index.items()]))
        # confirm trigram counts
        self.assertTrue(all([aka_index[name][1] == 2 for name in ['test', 'beta']]))
        self.assertTrue(all([aka_index[name][1] == 3 for name in ['alpha', 'theta', 'test2']]))
        self.assertTrue(all([aka_index[name][1] == 4 for name in ['alpha2', 'theta2']]))
        trigrams = {
            1: ['bet', 'ha2', 'ta2', 'st2'],
            2: ['tes', 'est', 'alp', 'lph', 'pha', 'the', 'het'],
            3: ['eta']
        }
        for count, keys in trigrams.items():
            for k in keys:
                self.assertEqual(len(trigram_product_index[k]), count)

        # set these manually for testing
        Trigram._aka_index = aka_index
        Trigram._product_index = trigram_product_index
        # test the matching algorithm
        match = Trigram.match('alpha')
        self.assertEqual(match[0], ('test', 'alpha', 1.0))
        self.assertEqual(match[1], ('test2', 'alpha2', 0.75))
        self.assertEqual(Trigram.match('none'), [])
