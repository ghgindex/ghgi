#!/usr/bin/env python3

try:
    from .convert import Convert
except:
    from convert import Convert
import re
import logging
from sre_constants import FAILURE
import nltk
from typing import Tuple
try:
    from .product import Product, Ingredient
except:
    from product import Product, Ingredient

logging.basicConfig(level=logging.INFO)


def case_insensitize(text):
    """ return a regex pattern that matches the input text regardless of casing """
    out = r''
    for char in text.lower():
        out += r'[{}{}]'.format(char, char.upper())
    return out


class Parser:
    """ Parse amount information and ingredient identification text
    from raw recipe text.
    """
    # --------- Standard attribute names --------- #
    MODS = Ingredient.MODS
    QTYS = Ingredient.QTYS
    EA = Ingredient.EA
    NAMES = Product.NAMES
    UNIT = 'UNIT'
    ALT_UNIT = 'ALT_UNIT'
    EA_UNIT = 'EA_UNIT'
    QUANTITY = 'QTY'
    ALT_QUANTITY = 'ALT_QTY'
    EA_QUANTITY = 'EA_QTY'
    AMOUNT = 'AMT'
    ALT_AMOUNT = 'ALT_AMT'
    EA_AMOUNT = 'EA_AMT'
    PLUS_AMOUNT = 'PLUS_AMT'
    INGREDIENT = 'INGRED'
    ALT_INGREDIENT = 'ALT_INGRED'

    # --------- Key punctuation --------- #
    OPEN_PARENTHESES = ['(', '[']
    CLOSE_PARENTHESES = [')', ']']

    # --------- Conversions and standardizations --------- #
    TEXT_NUMBERS = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10,
        'dozen': 12,
        'half-dozen': 6,
        'half dozen': 6,
        'half a dozen': 6
    }

    VULGAR_FRACTIONS = {
        u'\u00bc': '1/4',  # ¼
        u'\u00bd': '1/2',  # ½
        u'\u00be': '3/4',  # ¾
        u'\u2150': '1/7',  # ⅐
        u'\u2151': '1/9',  # ...
        u'\u2152': '1/10',
        u'\u2153': '1/3',
        u'\u2154': '2/3',
        u'\u2155': '1/5',
        u'\u2156': '2/5',
        u'\u2157': '3/5',
        u'\u2158': '4/5',
        u'\u2159': '1/6',
        u'\u215a': '5/6',
        u'\u215b': '1/8',
        u'\u215c': '3/8',
        u'\u215d': '5/8',
        u'\u215e': '7/8',
        u'\u215f': '',
        u'\u2189': '',
    }

    UNITS = {
        'ml': 'ml',
        'milliliter': 'ml',
        'millilitre': 'ml',
        'litre': 'l',
        'liter': 'l',
        'l': 'l',
        'g': 'g',
        'gram': 'g',
        'kg': 'kg',
        'kilo': 'kg',
        'kilogram': 'kg',
        'kilogramme': 'kg',
        'cup': 'cup',
        'c': 'cup',
        'tablespoon': 'tablespoon',
        'tbsp': 'tablespoon',
        'teaspoon': 'teaspoon',
        'tsp': 'teaspoon',
        'T': 'tablespoon',
        't': 'teaspoon',
        'pound': 'pound',
        'lb': 'pound',
        'ounce': 'ounce',
        'oz': 'ounce',
        'quart': 'quart',
        'qt': 'quart',
        'pint': 'pint',
        'pt': 'pint',
        'dash': 'dash',
        'pinch': 'pinch',
        'handful': 'handful',
        'fistful': 'fistful',
        'smidgen': 'smidgen',
        'bunch': 'bunch',
        'drop': 'drop',
        'ea': 'ea',
        'ear': 'ea',
        'slice': 'ea',
        'stalk': 'ea',
        'stick': 'ea',
        'sprig': 'ea',
        'can': 'pkg',
        'container': 'pkg',
        'package': 'pkg',
        'tin': 'pkg',
        'jar': 'pkg',
        'fillet': 'ea',
    }

    # --------- Stop/otherwise unhelpful words --------- #
    STOPWORDS = {
        # nltk base set (english) with 't', 'with', 'or', 'to', 'in', 'at', 'on', 'of' removed
        'had', 'few', 'under', 'an', 'its', 'why', 'were', 'all', 'doing',
        'while', 'how', 'don', 'same', 'is', 'because', 'him', 'ourselves', 'off',
        'herself', 'has', 'into', 'd', 'out', 'he', 'against', 'themselves',
        'wouldn', 'theirs', 'be', 'above', 'up', 'own', 'are', 'when',
        'through', 'will', 'by', 'our', 'who', 'between', 'so', 'ain', 'this',
        'than', 'aren', 'them', 'not', 'wasn', 'your', 'these', 'himself',  # 'of',
        'down', 'won', 'for', 'only', 'as', 'myself', 'both', 'yours', 'during',
        'you', 'too', 'where', 's', 'hadn', 'about', 'and', 'been', 'very', 'do',
        'over', 'most', 'o', 'that', 'was', 'again', 'further',
        'couldn', 'having', 'hasn', 'mightn', 'me', 'no', 'her', 'hers', 'ours',
        'haven', 'my', 'it', 'nor', 'those', 'she', 'what', 'a', 're',
        'but', 'just', 'once', 'whom', 'from', 'am', 'below', 'mustn', 'ma', 've',
        'the', 'more', 'll', 'didn', 'needn', 'then', 'isn', 'should', 'his',
        'before', 'doesn', 'm', 'did', 'yourself', 'other', 'yourselves',
        'itself', 'any', 'being', 'i', 'here', 'some', 'which', 'we', 'such',
        'there', 'weren', 'if', 'now', 'shan', 'after', 'they', 'shouldn', 'have',
        'their', 'y', 'does', 'until'
    }

    STOPWORDS |= {
        '',  # strip empty words (e.g. punctuation replacements)
        '~',
        'amount',
        'approx',
        'approximately',
        'approx.',
        'appr.',
        'assorted',
        'baby',
        'coarse',
        'coarsely',
        'cold',
        'cooled',
        'cored',
        'cut',
        'desired',
        'drizzling',
        'equal',
        'fillet',
        'fillets',
        'fine',
        'firm',
        'finely',
        'flaky',
        'fresh',  # leave this in for "fresh bean"?
        'freshly',
        'frozen',  # leave this in for "frozen pea"?
        'garnish',
        'garnishes',
        'gently',
        'grilled',
        'halved',
        'halves',
        'high-quality',
        'hulled',
        'interval',
        'kitchen',
        'like',
        'twine',
        'least',
        'leftover',
        'low-sodium',
        'medium',
        'mild',
        'optional',
        'organic',
        'peeled',
        'picked',
        'pitted',
        'plain',
        'preferably',
        'pure',
        'quartered',
        'ripe',
        'room',
        'roughly',
        'salted',
        'scrubbed',
        'seeded',
        'serving',
        'shredded',
        'similar',
        'softened',
        'stemmed',
        'store-bought',
        'taste',
        'temperature',
        'thawed',
        'thinly',
        'toasted',
        'trimmed',
        'unsalted',
        'unseasoned',
        'unsweetened',
        'washed',
    }

    PREP_MODS = {  # try to suss out preps that (might) affect density
        'beaten',
        'boned',
        'boneless',
        'canned',
        'chopped',
        'cleaned',
        'creamed',
        'crosswise',
        'crumbled',
        'crushed',
        'dice',
        'diced',
        'dissolved',
        'drained',
        'flaked',
        'freeze-dried',
        'generous',
        'grated',
        'ground',
        'gutted',
        'heaping',
        'jarred',
        'large',  # can be used to modify a quantity, e.g "large handful"
        'lengthwise',
        'lightly',
        'loosely',
        'melted',
        'minced',
        'packed',
        'pressed',
        'puree',
        'pureed',
        'roasted',
        'sauteed',
        'scaled',
        'shelled',
        'sifted',
        'skin-on',
        'skinless',
        'skinned',
        'sliced',
        'small',  # can be used to modify a quantity, e.g "small handful"
        'smashed',
        'smoked',
        'squeezed',
        'steamed',
        'tightly,'
        'torn',
        'well',
        'whipped',
        'whisked',
        'zested',
    }

    # --------- Unit regexes --------- #
    RE_UNIT_LABELS = [case_insensitize(unit) for unit in UNITS]
    RE_UNITS_GROUP = r'|'.join(RE_UNIT_LABELS)
    RE_UNITS_PLURAL = re.compile(r'({})([sei]*)$'.format(RE_UNITS_GROUP))

    # --------- Input text pre-processing --------- #
    @classmethod
    def preprocess(cls, text: str) -> Tuple[str, bool, bool]:
        """
        Return the cleaned text, and bools indicating if disregard should be sustained,
        or unsustained. If both bools are False, then disregard should be left as is
        Preprocess/standardize ingredient text in preparation for analysis:
            * Strip leading/trailing whitespace
            * Strip out any html tags
            * Expand vulgar fractions, prepending a space, e.g. "1¼" -> "1 1/4" (nltk takes 1/4 as a number, huzzah!)
            * Put a space between spaceless units, e.g. "6c" -> "6 c"
        """
        text = text.strip()  # remove leading/trailing whitespace
        text = cls.strip_html_tags(text)
        text = cls.devulgarize(text)
        text = cls.gap_units(text)
        disregard, sustain, unsustain = cls.disregard(text)
        if disregard:
            return None, sustain, unsustain

        return text, sustain, unsustain

    RE_GAPLESS_UNITS = re.compile(r'(\d)({})\b'.format(RE_UNITS_GROUP))

    @classmethod
    def gap_units(cls, text: str) -> str:
        """ Insert a space between quantities and units, e.g. '6c' -> '6 c' """
        return re.sub(cls.RE_GAPLESS_UNITS, r'\g<1> \g<2>', text)

    @classmethod
    def devulgarize(cls, text):
        """ Expand unicode vulgar fractions, prepending a space"""
        for k, v in cls.VULGAR_FRACTIONS.items():
            text = text.replace(k, ' ' + v)
        return text

    # strip_html_tags regexes
    RE_TAG_START = re.compile(r'<((a)|(strong)|(span)).*?>')
    RE_TAG_END = re.compile(r'</((a)|(strong)|(span))>')

    @classmethod
    def strip_html_tags(cls, text):
        # At some point, we need to decide the "correct" way to handle inlined
        # recipe links/whether we want to do anything about that
        return re.sub(cls.RE_TAG_END, '', re.sub(cls.RE_TAG_START, '', text))

    # disregard regexes
    RE_ALL_PARENS = re.compile(r'^\([^\)]*\)$')
    RE_COLON_ANYWHERE = re.compile(r'.*:.*')
    RE_TERMINAL_COLON = re.compile(r'.*:\s*$')
    # entries that cause subsequent entries to be disregarded as well
    RE_DISREGARD_SUSTAIN_HEADERS = [re.compile(r) for r in [
        r'equipment:\s*$',
        r'special equipment:\s*$',
        r'glass(ware)?:\s*$',
        r'note:\s*$',
        r'serving suggestion(s)?:\s*$',
        r'test-kitchen tip:\s*$',
        r'type of fire:\s*$',
    ]]

    # entries that cause subsequent entries to no longer be disregarded
    RE_DISREGARD_UNSUSTAIN_HEADERS = [re.compile(r) for r in [
        r'for .*:\s*$',
    ]]

    # cases where this entry should be disregarded
    RE_DISREGARD_HEADERS = [re.compile(r) for r in [
        r'accompaniments?:',
        r'for .*:',
        r'garnish(es)?:',
        r'glass(ware)?:',
        r'grill heat:',
        r'ingredient info:',
        r'note:',
        r'serving suggestion(s)?:',
        r'test-kitchen tip:',
        r'type of fire:',
        r'special equipment:',
        r'equipment:',
    ]]

    @classmethod
    def disregard(cls, text: str) -> Tuple[bool, bool, bool]:
        """ 
        Return a 3-tuple of booleans (disregard, sustain, unsustain). The first
        is whether this ingredient should be disregarded (i.e. if text isn't a
        "real" ingredient), the second is whether subsequent ingredients should
        also be be disregarded (usually because this ingredient indicates that
        what follows won't be ingredient info), and the third is whether any
        active disregard state should be turned off.

        Things that are marked optional remain TBD, but I lean towards disregarding these, too.
        """

        if not text:  # empty
            return True, False, False
        if re.match(cls.RE_TERMINAL_COLON, text):
            # Ends in a colon ":" (and any trailing whitespace) almost always means it's a directive.
            # There are a few cases where a quantity is provided as part of this,
            # but this is very rare, and more often than not the quantity is redundant
            # with subsequent entries. We'll live with the misses here.
            lowered = text.lower()
            if any([re.match(pttrn, lowered) for pttrn in cls.RE_DISREGARD_SUSTAIN_HEADERS]):
                return True, True, False

            if any([re.match(pttrn, lowered) for pttrn in cls.RE_DISREGARD_UNSUSTAIN_HEADERS]):
                return True, False, True

            return True, False, False

        if re.match(cls.RE_ALL_PARENS, text):
            # entirely parenthetical, e.g. "(Essential oil complement: orange)"
            return True, False, False

        if re.match(cls.RE_COLON_ANYWHERE, text):
            # check for certain other directives, which typically include a colon,
            # e.g. "Equipment:...", "Accompaniment:...", "Ingredient info:..."
            lowered = text.lower()
            # re.match only considers string start, which is what we want
            if any([re.match(pttrn, lowered) for pttrn in cls.RE_DISREGARD_HEADERS]):
                return True, False, False

        return False, False, False

    # --------- Tokenization --------- #
    @classmethod
    def tokenize(cls, text: str) -> list:
        """ A wrapper on nltk.word_tokenize, except when
        we see things like "grams/3" in the nltk tokens (e.g. from an ingredient that read
        "45 grams/3 ounces of oil"), replace it with "grams", "/", "3" so we can use the
        slash as an indicator of an alternative measure.
        """
        # tokenize and tag the text usin nltk defaults
        tokens = nltk.word_tokenize(text)
        out = []
        for t in tokens:
            if '/' not in t:
                out += [t]
                continue

            parts = t.split('/')
            digits = len(
                [el for el in parts if el[:1].isdigit() or el[-1:].isdigit()])
            if digits == len(parts):
                out += [t]
                continue

            for i, p in enumerate(parts):
                if p:  # don't include empty strings
                    out += [p]
                if i < len(parts) - 1:
                    out += ['/']

        out = [cls.numerify(el) for el in out]
        out = [cls.separate_qualifier_units(el) for el in out]
        out = [e for el in out for e in el]

        return out

    @classmethod
    def separate_qualifier_units(cls, text: str) -> list:
        tokens = text.split('-')
        if len(tokens) == 1:
            return [text]

        if re.match(cls.RE_UNITS_PLURAL, tokens[-1]):
            unit = tokens[-1]
            tokens[-1] = ''
            return '-'.join(tokens), unit

        return [text]

    @classmethod
    def numerify(cls, text: str) -> list:
        """ Convert text numbers to digits """
        tokens = text.split('-')

        if len(tokens) == 1:
            # no dashes present; tokens[0] == text
            return str(cls.TEXT_NUMBERS.get(text.lower(), text))
        elif not any([token.lower() in cls.TEXT_NUMBERS for token in tokens]):
            # no numbers
            return text

        # We have numeric text, which should only be converted to digits if
        # it's being used as a quantity (vs, most notably, five-spice powder)
        # or a range of quantities.
        # This means the token after a number must be either a unit, a range
        # indicator (to, or), or empty before we will convert it

        if len(tokens) == 2:
            if (not tokens[1]) or re.match(cls.RE_UNITS_PLURAL, tokens[1]):
                # e.g. "five-", "six-ounce"
                tokens[0] = cls.TEXT_NUMBERS.get(tokens[0].lower(), tokens[0])

        elif len(tokens) == 4 and re.match(cls.RE_UNITS_PLURAL, tokens[-1]) and tokens[1].lower() in ['or', 'to']:
            # e.g. "five-to-six-ounce"
            tokens = [cls.TEXT_NUMBERS.get(
                token.lower(), token) for token in tokens]

        return '-'.join([str(t) for t in tokens])

    # --------- Number unification --------- #
    @classmethod
    def decimate(cls, tokens: list) -> list:
        """ Convert fractions to decimals.
        Yes, the method name is cheeky.
        """
        out = []
        prev_digit = None
        for t in tokens:
            dash = ''
            if t.endswith('-'):
                t = t[:-1]
                dash = '-'

            parts = t.split('/')
            if len(parts) != 2:
                out += [t+dash]

            elif all([p.isdigit() for p in parts]):
                # `1/2`
                val = float(parts[0])/float(parts[1])
                if prev_digit:
                    # sum and overwrite
                    val += prev_digit
                    out[-1] = str(val) + dash
                else:
                    out += [str(val) + dash]

            elif parts[1].isdigit() and len(parts[0].split('-')) == 2 and all([p.isdigit() for p in parts[0].split('-')]):
                # `1-1/2`
                denominator = float(parts[1])
                whole, numerator = parts[0].split('-')
                val = float(whole) + float(numerator)/denominator
                out += [str(val) + dash]

            else:
                out += [t+dash]

            prev_digit = float(t) if t.isdigit() else None

        return out

    @classmethod
    def rangeify(cls, tokens: list) -> list:
        """
        Convert ranged numbers to their midpoints, e.g. `6 to 8` -> `7`.

        This does *not* range units, e.g. it excludes things like 
        `6 cups to 2 gallons` which will be done elsewhere TBD. 

        Trailing dashes are preserved.

        Covered formats:
            `6 to 8`
            `6-to-8`
            `6-to-8-`
        """
        out = []
        prev_value = None
        range_active = False
        for token in tokens:
            # look for numbers, numbers ending in dashes
            dash = ''
            if token[-1] == '-':
                dash = '-'
                token = token[:-1]

            if any([cc in token for cc in ['-to-', '-or-']]):
                cc = '-to-' if '-to-' in token else '-or-'
                parts = token.split(cc)
                try:
                    midpoint = (float(parts[0]) + float(parts[1])) / 2
                    out += [str(midpoint) + dash]
                except ValueError:
                    out += [token + dash]
                range_active = False
                prev_value = None

            elif token in ['or', 'to']:
                range_active = bool(prev_value)
                out += [token + dash]

            else:  # see if it's a number
                try:
                    val = float(token)
                    if range_active:
                        midpoint = (val + prev_value) / 2
                        out[-2:] = [str(midpoint) + dash]
                        prev_value = None
                    else:
                        out += [str(val) + dash]
                        prev_value = val
                except ValueError:
                    out += [token + dash]
                    prev_value = None
                range_active = False

        return out

    # --------- Ingredient tagging --------- #
    @classmethod
    def tag(cls, tokens: list) -> list:
        """
        This is the main semantic undertaking of the Parser. A series of steps
        build on each other to extract the amount information, and consolidate
        the remaining text to focus on useful words and phrases.
        """
        data = nltk.pos_tag(tokens)
        data = cls.tag_units_and_quantities(data)
        data = cls.coalesce_units(data)
        data = cls.tag_amounts(data)
        data = cls.tag_alt_amounts(data)
        data = cls.complete_amounts(data)
        data = cls.merge_amounts(data, cls.ALT_AMOUNT)
        data = cls.merge_amounts(data, cls.EA_AMOUNT)
        data = cls.strip_qualifier_parens(data)
        data = cls.strip_remnants(data)
        data = cls.plus_amounts(data)
        # hereafter, ingredients is a list of separate ingredients
        ingredients = cls.label_ingredients(data)
        # nltk doesn't do a great job when ingredient data is mixed in, so
        # re-pos_tag the leftovers to improve accuracy of POS values for the
        # focus() call that follows.
        ingredients = [cls.retag(i) for i in ingredients]
        ingredients = [cls.resolve_amounts(i) for i in ingredients]
        # hereafter, ingredients are a 3-tuple as we add a `mods` element
        ingredients = [cls.focus(i) for i in ingredients]
        ingredients = [cls.unstop(i) for i in ingredients]
        return ingredients

    @classmethod
    def tag_units_and_quantities(cls, tokens: list) -> list:
        # tag digit (CD) tokens with the QTY type
        # tag units tokens with the UNIT type
        out = []
        for token in tokens:
            if token[1] == 'CD':  # digit
                try:  # make sure it's actually a digit
                    float(token[0])
                    out += [(token[0], cls.QUANTITY)]
                except ValueError:
                    numeric = ''.join(
                        [s for s in token[0] if s in '1234567890.'])
                    try:
                        float(numeric)
                        out += [(numeric, cls.QUANTITY)]
                    except ValueError:
                        out += [token]
            elif re.match(cls.RE_UNITS_PLURAL, token[0]):
                out += [(token[0], cls.UNIT)]
            else:
                out += [token]
        return out

    @classmethod
    def coalesce_units(cls, tokens: list) -> list:
        # replace [UNIT]/[UNIT]/*, [UNIT] or [UNIT], and [UNIT], [UNIT] with first unit
        out = []
        prev_unit = False
        for token in tokens:
            if token[1] == cls.UNIT:
                if prev_unit:
                    trunc = False
                    while out[-1][0] in ['/', 'or', ',']:
                        out = out[:-1]
                        trunc = True
                    if trunc:
                        continue
                else:
                    prev_unit = True
            elif prev_unit and token[0] not in ['/', 'or', ',']:
                prev_unit = False
            out += [token]
        return out

    RE_QQR = re.compile(r'[\d\.]+-$')

    @classmethod
    def tag_amounts(cls, tokens: list) -> list:
        # tag quantities that are qualifiers, as identified by a trailing dash,
        # tag their subsequent units and EA_UNITS, and aggregate them with
        # their units into a EA_AMOUNT. tag non-qualifier amounts as AMOUNT.
        out = []
        approximators = ['about', 'approx', 'approx.', 'approximately']
        skip = False
        for i, token in enumerate(tokens):
            if skip:
                skip = False
                continue
            if re.match(cls.RE_QQR, token[0]):
                # drop the trailing dash and mark as an EA_QUANTITY
                out += [(token[0][:-1], cls.EA_QUANTITY)]
            elif token[1] == cls.UNIT and i > 0 and out[-1][1] == cls.QUANTITY:
                if len(tokens) > i + 1 and tokens[i+1][0][:4] in ['each']:
                    out[-1] = [[(out[-1][0], cls.EA_QUANTITY),
                                (token[0], cls.EA_UNIT)], cls.EA_AMOUNT]
                    # also check for a preceding paired amount and convert to an EA_AMOUNT
                    # this may not cover all possible cases!
                    if len(out) > 2 and out[-2][0] in ['/', 'or'] and out[-3][1] == cls.AMOUNT:
                        # mark its paired amount as an EA_AMOUNT
                        out[-3] = [out[-3][0], cls.EA_AMOUNT]
                    # look for any preceding approximator and remove it
                    if len(out) > 1 and out[-2][0] in approximators:
                        out = out[:-3] + [out[-1]]
                    skip = True  # skip the following 'each'
                elif len(out) > 2 and out[-2][0] in approximators:
                    # check for 'about' or 'approx*' before this, which indicates an ALT_AMOUNT
                    out[-2] = [[(out[-1][0], cls.ALT_QUANTITY),
                                (token[0], cls.ALT_UNIT)], cls.ALT_AMOUNT]
                    out = out[:-1]
                else:
                    out[-1] = [[out[-1], token], cls.AMOUNT]
            elif token[1] == cls.UNIT and i > 0 and out[-1][1] == cls.EA_QUANTITY:
                out[-1] = [[out[-1], (token[0], cls.EA_UNIT)], cls.EA_AMOUNT]
            else:
                out += [token]
        return out

    @classmethod
    def tag_alt_amounts(cls, tokens: list) -> list:
        # Tag alt amounts as indicated by amounts following other amounts,
        # either in parentheses or separated by slashes.
        out = []
        prev_type = None
        alt_active = False
        multiple_alts = False
        for token in tokens:
            if prev_type not in [cls.AMOUNT, cls.ALT_AMOUNT, cls.EA_AMOUNT]:
                prev_type = token[1]

            elif token[0] in ['(', '[', '/', 'or']:
                alt_active = True
                multiple_alts = token[0] in ['(', '[']

            elif not alt_active:
                prev_type = token[1]

            elif token[1] == cls.AMOUNT:
                # retag it as an ALT_AMOUNT incl. ALT_QUANTITY and ALT_UNIT
                for i in range(len(token[0])):
                    if token[0][i][1] == cls.QUANTITY:
                        token[0][i] = (token[0][i][0], cls.ALT_QUANTITY)
                    elif token[0][i][1] == cls.UNIT:
                        token[0][i] = (token[0][i][0], cls.ALT_UNIT)
                token[1] = cls.ALT_AMOUNT

                if not multiple_alts:
                    alt_active = False
                    multiple_alts = False

            elif token[0] in [')', ']']:
                alt_active = False
                multiple_alts = False

            out += [token]

        return out

    @classmethod
    def complete_amounts(cls, tokens: list) -> list:
        """ Pull QTY or UNIT values back to orphaned partners, filling in the
        blanks if none are found. Do NOT complete parenthetical orphaned QTYs,
        as this is usually not actual quantity information.
        """
        out = []
        qty_index = None
        unit_index = None
        any_qty = False
        any_unit = False
        any_amt = False
        parenthetical = False
        for i, token in enumerate(tokens):
            if token[0] in cls.OPEN_PARENTHESES:
                parenthetical = True
            elif parenthetical and token[0] in cls.CLOSE_PARENTHESES:
                parenthetical = False
            if token[1] == cls.UNIT:
                any_unit = True
                if qty_index is not None:
                    # this is the unit for the existing qty
                    out[qty_index] = [[out[qty_index], token], cls.AMOUNT]
                    qty_index = None
                    continue
                elif unit_index is not None:
                    # default to qty 1 for existing unit_index
                    out[unit_index] = [
                        [('1', cls.QUANTITY), out[unit_index]], cls.AMOUNT]
                unit_index = len(out)
                # out += [token]
            elif token[1] == cls.QUANTITY and not parenthetical:
                any_qty = True
                if qty_index is not None:
                    # existing qty is an orphan; default unit to `ea`
                    out[qty_index] = [
                        [out[qty_index], (cls.EA, cls.UNIT)], cls.AMOUNT]
                qty_index = len(out)
                # out += [token]
            elif token[1] == cls.AMOUNT:
                any_amt = True
            out += [token]

        # clean up any units/qtys left hanging at the end
        if qty_index is not None:
            out[qty_index] = [
                [out[qty_index], (cls.EA, cls.UNIT)], cls.AMOUNT]

        if unit_index is not None:
            out[unit_index] = [
                [('1', cls.QUANTITY), out[unit_index]], cls.AMOUNT]
            if unit_index > 0 and out[unit_index-1][1] == cls.EA_AMOUNT:
                # if hanging unit was preceded by an EA_AMOUNT, flip the AMOUNT before
                # the EA_AMOUNT
                out[unit_index-1:unit_index +
                    1] = [out[unit_index], out[unit_index-1]]

        if not (any_amt or any_unit or any_qty):
            out = [[[('1', cls.QUANTITY), (cls.EA, cls.UNIT)],
                    cls.AMOUNT]] + out

        return out

    @classmethod
    def merge_amounts(cls, tokens: list, merge_flavor) -> list:
        # link ALT_AMOUNTs to their parent AMOUNT or EA_AMOUNT,
        # and link EA_AMOUNTS to their parent AMOUNT
        out = []
        prev_par_index = None

        for token in tokens:
            if not token[1] == merge_flavor:
                out += [token]

            if token[1] == merge_flavor:
                if prev_par_index is not None:
                    out[prev_par_index][0] += [token]
                else:
                    out += [token]
            elif token[1] in [cls.AMOUNT, cls.EA_AMOUNT]:
                # order of this and previous elif matter because EA_AMOUNT
                # cannot be a parent if it's the merge_flavor
                prev_par_index = len(out) - 1

        return out

    @classmethod
    def strip_qualifier_parens(cls, tokens: list) -> list:
        # Remove parentheticals, preserving only qualifier amount(s).
        # if the parenthetical starts with "or AMT", remove the parentheses but
        # otherwise preserve it
        paren_indexes = []
        cur_paren_index = []
        parens_only = False
        for i, token in enumerate(tokens):
            if token[0] in cls.OPEN_PARENTHESES:
                cur_paren_index += [i]
                if len(tokens) > i + 2:
                    if type(tokens[i+1][0]) is str and tokens[i+1][0].lower() in ['or']:
                        if tokens[i+2][1] in [cls.AMOUNT, cls.ALT_UNIT, cls.EA_AMOUNT]:
                            parens_only = True
            elif token[0] in cls.CLOSE_PARENTHESES:
                if cur_paren_index:
                    cur_paren_index += [i]
                    paren_indexes += cur_paren_index
                    cur_paren_index = []  # reset
                    parens_only = False
            elif cur_paren_index and token[1] not in [cls.EA_AMOUNT, cls.ALT_AMOUNT, cls.AMOUNT] and not parens_only:
                cur_paren_index += [i]

        return [t for i, t in enumerate(tokens) if i not in paren_indexes]

    @classmethod
    def strip_remnants(cls, tokens: list) -> list:
        # Remove leftover things like slashes that separated amounts.
        # Currently looks for slashes and 'of'
        out = []
        prev_flavor = None

        for token in tokens:
            if token[0] in ['/', 'of'] and prev_flavor in [cls.AMOUNT, cls.EA_AMOUNT, cls.ALT_AMOUNT]:
                continue
            out += [token]
            prev_flavor = token[1]

        return out

    @classmethod
    def plus_amounts(cls, tokens: list) -> list:
        # If we find the pattern [AMT, 'plus', AMT], append the second
        # AMT to the first one and change its type to Parser.PLUS_AMOUNT
        out = []
        for i, token in enumerate(tokens):
            if token[1] in [cls.AMOUNT]:
                # handle this via lookbehind
                if i > 1:
                    prev_token = tokens[i-1][0]
                    if type(prev_token) is str and prev_token.lower() in ['plus']:
                        prev_prev_token = tokens[i-2]
                        if prev_prev_token[1] in [cls.AMOUNT]:
                            out[-2][0] += [(token[0], cls.PLUS_AMOUNT)]
                            out = out[:-1]
                            continue
            out += [token]
        return out

    @classmethod
    def label_ingredients(cls, tokens: list) -> list:
        # Sometimes an ingredient line contains two separate ingredients,
        # usually because the second one is provided as an alternative.
        # Here, we wrap ingredients in either Parser.INGREDIENT, or Parser.ALT_INGREDIENT
        # tags if full ingredients are separated by an 'or' token.
        # We also want to pull amounts to the front of ingredients if they don't already
        # have one.
        # This has quite limited capabilities and will need to be evolved.
        ingred = []
        ingred_amt = False
        ingred_name = False
        ingred_has_lead_amt = False
        or_index = None
        out = []
        for token in tokens:
            if token[1] in [cls.AMOUNT, cls.ALT_AMOUNT, cls.EA_AMOUNT]:
                if ingred_amt and ingred_name and (or_index is not None):
                    # we've already parsed a full ingredient; start a new one
                    if out:
                        out += [[ingred, cls.ALT_INGREDIENT]]
                    else:
                        del ingred[or_index]
                        out += [[ingred, cls.INGREDIENT]]
                    ingred = []  # reset
                    ingred_name = False
                    or_index = None
                    ingred_has_lead_amt = False
                ingred_amt = True
            elif type(token[1]) is str:
                if token[1].startswith('NN'):
                    ingred_name = True
                elif token[0].lower() == 'or' and ingred_name and ingred_amt:
                    # only count this if we've seen the rest of the ingredient
                    or_index = len(ingred)

            if token[1] in [cls.AMOUNT, cls.ALT_AMOUNT, cls.EA_AMOUNT] and not ingred_has_lead_amt:
                # move amount to the front only if the ingred doesn't already have an amount
                ingred = [token] + ingred  # prepend
                ingred_has_lead_amt = True
            else:
                ingred += [token]

        if ingred:
            flavor = cls.ALT_INGREDIENT if out else cls.INGREDIENT
            out += [[ingred, flavor]]

        return out

    @classmethod
    def retag(cls, ingredient: list) -> list:
        """ 
        Retag the remaining words once the amount info has been removed, 
        parsing the biggest chunks possible to maximize the info given to nltk.
        """
        # Find any ingredient bits that aren't strings!
        non_string_indexes = [i for i in range(
            len(ingredient[0])) if type(ingredient[0][i][0]) is not str]
        # now, move pairwise through the non_string_index values, re-tagging
        # whatever's in between those indexes
        prev = 0
        for i in non_string_indexes:
            ingredient[0][prev:i] = nltk.pos_tag(
                [ing[0] for ing in ingredient[0][prev:i]])
            prev = i + 1
        ingredient[0][prev:] = nltk.pos_tag(
            [ing[0] for ing in ingredient[0][prev:]])
        return ingredient

    @classmethod
    def resolve_amounts(cls, ingredient: list) -> list:
        resolved = []
        for token in ingredient[0]:
            if token[1] not in [cls.AMOUNT, cls.EA_AMOUNT, cls.ALT_AMOUNT]:
                resolved += [token]
                continue
            qty, unit = cls.quantify(token[0])
            resolved += [[[(qty, cls.QUANTITY), (unit, cls.UNIT)], token[1]]]
        return [resolved, ingredient[1]]

    @classmethod
    def focus(cls, ingredient: list, mods: list = None) -> list:
        """
        Remove extraneous things like prep mods and unhelpful descriptions.
        This is mostly done using parts of speech and their position in the ingredient.
        We call this recursively as we eliminate unhelpful bits.
        """
        ingred = ingredient[0]
        pos_distractions = ['VBD', 'VBN', 'IN', 'DT']
        distractions = ['preferably']
        mods = [] if mods is None else mods

        if ingred[-1][0] in [',', ';', '.']:
            # eliminate dangling punctuation
            ingred = ingred[:-1]
            return cls.focus([ingred, ingredient[1]], mods)

        first_noun = [i for i in range(len(ingred)) if type(
            ingred[i][1]) is str and ingred[i][1].startswith('NN')]
        first_noun = min(first_noun) if first_noun else 0

        # find the comma indexes, which often delineate phrases
        commas = [i for i in range(len(ingred)) if ingred[i][0] in [
            ','] and i > first_noun]
        if commas:
            # TODO: this bails as soon as it finds one useful phrase; it should continue to
            # backtrack and see if there's anything else to snip out!
            phrase = ingred[commas[-1]+1:]
            if phrase[0][1] in pos_distractions or phrase[-1][1] in pos_distractions or phrase[0][0] in distractions:
                cruft = ingred[commas[-1]:]
                mods += [c[0]
                         for c in cruft if type(c[0]) is str and c[0].lower() in cls.PREP_MODS]
                ingred = ingred[:commas[-1]]
                return cls.focus([ingred, ingredient[1]], mods)

        # fix cruft in the lede phrase
        noun_seen = False
        distraction_start = None
        lede_pos_distractions = ['VBD', 'VBN', 'DT']
        lede_destractions = ['in']

        for i, el in enumerate(ingred):
            if not noun_seen and type(el[1]) is str and el[1].startswith('NN'):
                noun_seen = True
            elif noun_seen and (distraction_start is None) and (el[1] in lede_pos_distractions or el[0] in lede_destractions):
                distraction_start = i
            elif noun_seen and el[0] == ',':
                break

        if distraction_start is not None:
            # snip it out, preserving any mods
            distraction = ingred[distraction_start:i]
            mods += [d[0]
                     for d in distraction if type(d[0]) is str and d[0].lower() in cls.PREP_MODS]
            ingred = ingred[:distraction_start] + ingred[i+1:]

        # there can also be cruft prior to the lede phrase; remove it
        prior_phrases = [i for i in range(len(ingred)) if ingred[i][0] in [
            ','] and i < first_noun]
        non_amts = [i for i in range(len(ingred)) if ingred[i][1] not in [
            cls.AMOUNT, cls.EA_AMOUNT, cls.ALT_AMOUNT]]
        non_amt_start = min(non_amts) if non_amts else None
        if prior_phrases and (non_amt_start is not None):
            phrase = ingred[non_amt_start:prior_phrases[0]+1]
            if len(phrase) == 1 or phrase[0][1] in distractions or phrase[-1][1] in distractions:
                # snip it out, preserving any mods
                cruft = ingred[non_amt_start:prior_phrases[0]]
                mods += [c[0]
                         for c in cruft if type(c[0]) is str and c[0].lower() in cls.PREP_MODS]
                ingred = ingred[:non_amt_start] + ingred[prior_phrases[0]+1:]
                return cls.focus([ingred, ingredient[1]], mods)

        return [ingred, ingredient[1], mods]

    @classmethod
    def unstop(cls, ingredient: list) -> list:
        """ Remove stopwords and prep mods from parsed ingredient"""
        out = []
        prev_token = None
        mods = []
        for token in ingredient[0]:
            if type(token[0]) is str:
                if token[0].lower() in cls.STOPWORDS:
                    continue
                elif token[0].lower() in cls.PREP_MODS:
                    mods += [token[0]]
                    continue
            if token[0] == ',' and prev_token in [',', None]:
                prev_token = token[0]
                continue
            out += [token]
            if type(token[0]) is str:
                prev_token = token[0]
        # clean up dangling cruft left by removal of stopwords
        while out and out[-1][1] in ['CC', ',', 'TO']:
            del out[-1]
        return [out, ingredient[1], ingredient[2] + mods]

    # --------- Resolution of Parser.AMOUNTs and remnant strings
    #  to definitive quantities and single strings --------- #

    @classmethod
    def standardize_unit(cls, unit):
        """ Convert unit to its standard representation """
        if unit in cls.UNITS:
            return cls.UNITS[unit]
        elif unit[-1] == 's' and unit[:-1] in cls.UNITS:
            return cls.UNITS[unit[:-1]]
        elif unit[:-2] == 'es' and unit[:-2] in cls.UNITS:
            return cls.UNITS[unit[:-2]]

    @classmethod
    def quantify(cls, amount):
        """ Convert a Parser.AMOUNT object into a mass, volume, or `each` quantity,
        return a (quantity, unit) tuple. mass's unit is `g`, volume is `ml`,
        and each is `each`.

        Mass is preferred to volume; volume is preferred to `each`. Parse the amount,
        and standardize it to the most preferred option available.
        """
        qty, unit = None, None
        for el in amount[:2]:
            if len(el) > 1:
                if el[1] in [cls.QUANTITY, cls.EA_QUANTITY, cls.ALT_QUANTITY]:
                    qty = float(el[0])
                elif el[1] in [cls.UNIT, cls.EA_UNIT, cls.ALT_UNIT]:
                    unit = el[0]

        unit = cls.standardize_unit(unit)
        if unit in Convert.VOLUME:
            qty *= Convert.VOLUME[unit]
            unit = 'ml'

        elif unit in Convert.MASS:
            qty *= Convert.MASS[unit]
            unit = 'g'

        alt_amount = None
        plus_amount = None
        ea_amount = None
        for extra in amount[2:]:
            if extra[1] == cls.ALT_AMOUNT:
                alt_amount = cls.quantify(extra[0])
            elif extra[1] == cls.EA_AMOUNT:
                ea_amount = cls.quantify(extra[0])
            elif extra[1] == cls.PLUS_AMOUNT:
                plus_amount = cls.quantify(extra[0])

        # the order here matters, as we want to convert in reverse
        # order of priority, so that, for example, `ea` values get swapped out
        # before we assess `g`-specific modifications
        if unit in ['ea', 'pkg']:
            if ea_amount:
                qty *= ea_amount[0]
                unit = ea_amount[1]
            elif alt_amount and alt_amount[1] in ['g', 'ml']:
                qty, unit = alt_amount

        if unit == 'ml':
            if alt_amount and alt_amount[1] == 'g':
                qty, unit = alt_amount
            elif plus_amount and plus_amount[1] == 'ml':
                qty += plus_amount[0]

        if unit == 'g':
            # if we have a mass value, we only care about plus_amounts
            if plus_amount and plus_amount[1] == 'g':
                qty += plus_amount[0]

        return qty, unit

    @classmethod
    def detokenize(cls, ingredient_tokens):
        out = ''
        for t in ingredient_tokens:
            if out and t[1] not in [',']:
                out += ' '
            if t[1] in [cls.AMOUNT, cls.EA_AMOUNT, cls.ALT_AMOUNT]:
                # out += f'{t[0][0][0]} {t[0][1][0]}'
                continue
            else:
                if t[1] in [',', 'CC', '.'] and not out:
                    continue  # disregard leading cruft
                try:
                    out += t[0]
                except Exception as err:
                    print(t)
                    raise err
        return out

    @classmethod
    def parse(cls, raw_text: str, disregard_active: bool = False) -> Tuple[dict, bool]:
        """ Extract quantity and name information from an ingredient's `raw_text`,
        returning it as a dictionary, as well as a flag indicating whether subsequent
        entries should (continue to) be disregarded.

        `disregard_active` means that a previously parsed ingredient in this recipe
        returned `True` for the flag boolean in its call to `parse`. This usually 
        means that a previous ingredient was a header indicating that non-ingredient
        information follows, e.g. "Equipment:".

        In some cases, at least conceptually, `disregard_active` can be toggled back off,
        for instance if a subsequent header entry indicates that ingredient information
        might follow, e.g. "For the filling:". In that case, we would return ({}, False)
        to indicate that while this ingredient entry has no information, subsequent ones
        are expected to.
        """
        text, sustain, unsustain = cls.preprocess(raw_text)

        if disregard_active:
            return {}, not unsustain

        if text is None:
            return {}, sustain

        data = {}
        tokens = cls.tokenize(text)
        tokens = cls.decimate(tokens)
        tokens = cls.rangeify(tokens)

        tagged_data = cls.tag(tokens)
        # TODO: figure out what to do about "for example", "like", "such as" phrases

        if not tagged_data:
            return data, disregard_active

        # return tagged_data in the format it already knows!
        tagged_data = tagged_data[0]  # only use the first entry for now
        data = {
            cls.QTYS: [],
            cls.NAMES: [],
            cls.MODS: tagged_data[2],
        }
        while tagged_data[0] and tagged_data[0][0][1] == cls.AMOUNT:
            amt = tagged_data[0].pop(0)
            data[cls.QTYS] += [{el[1].lower(): el[0]
                                for el in amt[0]}]
        if tagged_data and tagged_data[0]:  # remnant
            data[cls.NAMES] = [cls.detokenize(tagged_data[0])]

        return data, disregard_active
