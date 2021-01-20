import os
import json
from enum import Enum
from .datasets import ORIGINS


class UnknownOriginException(Exception):
    pass


class GHGFlavor(Enum):
    """ GHGFlavor indexes the different GHG values available in the database
    as follows:
        * P_10 is the 10th percentile value for GHG emissions, i.e. the most
        optimistic available estimate
        * MEAN is the mean value
        * MEDIAN is the median value
        * P_90 is the 90th percentile, i.e. the most pessimistic available

    We may also add GHG_MIN and GHG_MAX, although the utility of these for our
    purposes is questionable.
    """
    P_10 = 0
    MEAN = 1
    MEDIAN = 2
    P_90 = 3


class Origin:
    _db = {}
    ORIGIN_PATHS = {}
    DEFAULT = None
    SUPER = 'super'
    for root, dirs, files in os.walk(ORIGINS, topdown=True):
        # index the origin data files for retrieval as needed
        for name in files:
            if not name.endswith('.json'):
                continue
            if not DEFAULT:
                # topdown means the first file is the parent (global.json)
                DEFAULT = name[:-5]
            ORIGIN_PATHS[name[:-5]] = os.path.join(root, name)

    ORIGINS = list(ORIGIN_PATHS.keys())

    @classmethod
    def load(cls, origin):
        if origin not in cls._db:
            # lazy load the data files
            if origin not in cls.ORIGINS:
                raise UnknownOriginException(
                    'Origin {} not found in database'.format(origin))
            with open(cls.ORIGIN_PATHS[origin]) as o:
                cls._db[origin] = json.load(o)

    @classmethod
    def values(cls, origin, product):
        """ return the best available values for this product and origin
        tree from the database. If no data is available and the origin has no
        super, return None.
        """
        if origin not in cls._db:
            cls.load(origin)

        # if the data is available for this origin, return it
        if product in cls._db[origin]:
            return cls._db[origin][product]

        # if the origin has a super, try that
        if cls._db[origin].get(cls.SUPER):
            return cls.values(cls._db[origin][cls.SUPER], product)

    @classmethod
    def ghg_value(cls, product, origin, flavor: GHGFlavor):
        """ if available, return the flavor value for this product and origin
        combo
        """
        if not origin:
            origin = cls.DEFAULT
        if origin not in cls.ORIGINS:
            raise UnknownOriginException(
                'Origin {} not found in database'.format(origin))
        if not flavor:
            flavor = GHGFlavor.MEAN

        values = cls.values(origin, product)
        if values is not None:
            return values[1][flavor.value]
