import os

from datasets import ORIGINS

class UnknownOriginException(Exception):
    pass

class Origin:
    _db = {}
    ORIGIN_PATHS = {}
    DEFAULT = None
    SUPER = 'super'
    for root, dirs, files in os.walk(ORIGINS):
        for name in files:
            if not name.endswith('.json'):
                continue
            if not DEFAULT:
                # this is the topmost file, i.e. global.json
                DEFAULT = name[:-5]
            ORIGIN_PATHS[name[:-5]] = os.path.join(root, name)

    ORIGINS = list(ORIGIN_PATHS.keys())
    # GHG flavor indexes
    GHG_10 = 0
    GHG_MEAN = 1
    GHG_MEDIAN = 2
    GHG_90 = 3


    @classmethod
    def values(cls, origin, product):
        if origin not in cls._db:
            if origin not in cls.ORIGINS:
                raise UnknownOriginException('Origin {} not found in database'.format(origin))
            with open(cls.ORIGINS[origin]) as o:
                cls._db[origin] = json.load(o)
        
        if product in cls._db[origin]:
            return cls._db[origin][product]
        
        if cls._db[origin].get(cls.SUPER):
            return cls.values(cls._db[origin][cls.SUPER], product)


    @classmethod
    def ghg_value(cls, flavor, product, origin):
        if not origin:
            origin = cls.DEFAULT
        if origin not in cls.ORIGINS:
            raise UnknownOriginException('Origin {} not found in database'.format(origin))
        
        values = cls.values(origin, product)
        if values is not None:
            return values[1][flavor]
