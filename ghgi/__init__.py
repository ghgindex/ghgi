from .datasets import *
import os
import pathlib

os.environ['NLTK_DATA'] = os.path.join(
    pathlib.Path(__file__).parent, 'nltk_data')

VERSION = '2021-10-03-1'
