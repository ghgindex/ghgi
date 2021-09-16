from unittest import TestCase

from ghgi.parser import amounts, pad_parentheses, devulgarize, pad_punctuation, clean, match_units, numerify
from ghgi.parser import STOPWORDS, PREP_MODS
from ghgi.trigram import Trigram
from .fixtures.parser import REGEX_UNITS_DATA
from .fixtures.parser import AMOUNTS_DATA
from .fixtures.parser import PARENS_DATA
from .fixtures.parser import VULGAR_DATA
from .fixtures.parser import SLASH_DATA
from .fixtures.parser import CLEAN_DATA


class TestRegexes(TestCase):
    def test_units_match(self):
        for line in REGEX_UNITS_DATA:
            matched_units = match_units(line[0])
            for i, output in enumerate(line[1]):
                self.assertEqual(matched_units[i][2], output)


class TestParser(TestCase):

    def test_amounts(self):
        for line in AMOUNTS_DATA:
            self.assertEqual(amounts(line[0]), line[1])

    def test_pad_parentheses(self):
        for line in PARENS_DATA:
            self.assertEqual(pad_parentheses(line[0]), line[1])

    def test_devulgarize(self):
        for line in VULGAR_DATA:
            self.assertEqual(devulgarize(line[0]), line[1])

    def test_pad_slashes(self):
        for line in SLASH_DATA:
            self.assertEqual(pad_punctuation(line[0]), line[1])

    def test_clean(self):
        for line in CLEAN_DATA:
            self.assertEqual(clean(line[0]), line[1])

    def test_stopword_safety(self):
        # ensure no stopword conflicts with aliases
        for k in Trigram.aka_index():
            self.assertFalse(k in STOPWORDS)
            for word in k.split():
                if word in STOPWORDS:
                    print('WARNING: stopword `{}` used in {}'.format(word, k))
                # self.assertFalse(word in STOPWORDS)

    def test_mods_safety(self):
        # ensure no mod conflicts with aliases
        for k in Trigram.aka_index():
            self.assertFalse(k in PREP_MODS)
            for word in k.split():
                if word in PREP_MODS:
                    print('WARNING: prep_mod `{}` used in {}'.format(word, k))
                # self.assertFalse(word in PREP_MODS)

    def test_names_mods(self):
        # coming soon!
        pass
