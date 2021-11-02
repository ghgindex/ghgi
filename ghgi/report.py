#!/usr/bin/env python
from ghgi.product import Product
import json


from .trigram import build_indexes
from .gin import GIN
from .datasets import SOURCE_PRODUCTS, SOURCE_FOOD_VALUES
from .datasets import MASTER_GIN_INDEX
from .origin import Origin, GHGFlavor
from .datasets import MASTER_PRODUCTS, MASTER_AKA_INDEX, MASTER_TRIGRAM_INDEX


def reference_products():
    # spit out the reference products for each food category
    print(json.dumps(Product.expanded_baselines(), indent=2))
    print(json.dumps(Product.efficiency_baselines(), indent=2))


if __name__ == "__main__":
    reference_products()
