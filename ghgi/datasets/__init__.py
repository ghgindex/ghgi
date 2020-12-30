import os
import pathlib

DATASETS = pathlib.Path(__file__).parent.absolute()

MASTER = os.path.join(DATASETS, 'master')
SOURCE = os.path.join(DATASETS, 'source')
LOCAL = os.path.join(DATASETS, 'localizations')

from .source import SOURCE_PRODUCTS
SOURCE_PRODUCTS = os.path.join(SOURCE, SOURCE_PRODUCTS)

from .master import MASTER_PRODUCTS, MASTER_AKA_INDEX, MASTER_TRIGRAM_INDEX
MASTER_PRODUCTS = os.path.join(MASTER, MASTER_PRODUCTS)
MASTER_AKA_INDEX = os.path.join(MASTER, MASTER_AKA_INDEX)
MASTER_TRIGRAM_INDEX = os.path.join(MASTER, MASTER_TRIGRAM_INDEX)

ORIGINS = os.path.join(MASTER, 'origins')