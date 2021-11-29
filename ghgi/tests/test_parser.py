from unittest import TestCase

from ghgi.parser import Parser
# amounts, pad_parentheses, devulgarize, pad_punctuation, clean, match_units, numerify
# from ghgi.parser import STOPWORDS, PREP_MODS
from ghgi.trigram import Trigram
from .fixtures.parser import REGEX_UNITS_DATA
from .fixtures.parser import AMOUNTS_DATA
# from .fixtures.parser import PARENS_DATA
from .fixtures.parser import VULGAR_DATA
# from .fixtures.parser import SLASH_DATA
from .fixtures.parser import CLEAN_DATA


# Deprecated, but semi-reworked to test the parser
class TestRegexes(TestCase):
    def test_units_match(self):
        for line in REGEX_UNITS_DATA:
            self.assertEqual(Parser.parse(line[0])[0], line[1])


class TestParser(TestCase):

    def test_parse(self):
        for line in AMOUNTS_DATA:
            self.assertEqual(Parser.parse(line[0])[0], line[1])

    def test_devulgarize(self):
        for line in VULGAR_DATA:
            self.assertEqual(Parser.devulgarize(line[0]), line[1])

    def test_stopword_safety(self):
        # ensure no stopword conflicts with aliases
        for k in Trigram.aka_index():
            self.assertFalse(k in Parser.STOPWORDS)
            for word in k.split():
                if word in Parser.STOPWORDS:
                    print('WARNING: stopword `{}` used in {}'.format(word, k))

    def test_mods_safety(self):
        # ensure no mod conflicts with aliases
        for k in Trigram.aka_index():
            self.assertFalse(k in Parser.PREP_MODS)
            for word in k.split():
                if word in Parser.PREP_MODS:
                    print('WARNING: prep_mod `{}` used in {}'.format(word, k))

    def test_names_mods(self):
        # coming soon!
        pass
