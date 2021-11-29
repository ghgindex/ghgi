from unittest import TestCase
from ghgi.gin import GIN
from .fixtures.gin import QUERIES


class TestGin(TestCase):
    def test_queries(self):
        # import pdb
        # pdb.set_trace()
        for q, result in QUERIES:
            print(q)
            print(result)
            self.assertEqual(result, GIN.query(q))
