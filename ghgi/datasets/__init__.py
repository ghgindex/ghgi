import os
import pathlib
from .master import MASTER_PRODUCTS, MASTER_AKA_INDEX, MASTER_TRIGRAM_INDEX, MASTER_GIN_INDEX
from .source import SOURCE_PRODUCTS, SOURCE_REFERENCES, SOURCE_FOOD_VALUES

DATASETS = pathlib.Path(__file__).parent.absolute()

MASTER = os.path.join(DATASETS, 'master')
SOURCE = os.path.join(DATASETS, 'source')
LOCAL = os.path.join(DATASETS, 'localizations')

SOURCE_PRODUCTS = os.path.join(SOURCE, SOURCE_PRODUCTS)
SOURCE_REFERENCES = os.path.join(SOURCE, SOURCE_REFERENCES)
SOURCE_FOOD_VALUES = os.path.join(SOURCE, SOURCE_FOOD_VALUES)

MASTER_PRODUCTS = os.path.join(MASTER, MASTER_PRODUCTS)
MASTER_AKA_INDEX = os.path.join(MASTER, MASTER_AKA_INDEX)
MASTER_TRIGRAM_INDEX = os.path.join(MASTER, MASTER_TRIGRAM_INDEX)
MASTER_GIN_INDEX = os.path.join(MASTER, MASTER_GIN_INDEX)

ORIGINS = os.path.join(MASTER, 'origins')

REFERENCES = os.path.join(MASTER, 'references.json')
