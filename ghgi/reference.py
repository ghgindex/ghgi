import json
from .datasets import REFERENCES


class Reference:
    _db = {}

    @classmethod
    def load(cls):
        with open(REFERENCES) as r:
            cls._db = json.load(r)

    @classmethod
    def db(cls):
        if not cls._db:
            cls.load()
        return cls._db
