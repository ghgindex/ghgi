from unittest import TestCase
from ghgi.gin import GIN
from .fixtures.gin import QUERIES


class TestGin(TestCase):
    def test_queries(self):
        for q, result in QUERIES:
            self.assertEqual(result, GIN.query(q))
