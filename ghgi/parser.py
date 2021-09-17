#!/usr/bin/env python3

import re
import logging
import inflect
p = inflect.engine()

logging.basicConfig(level=logging.INFO)

MODS = 'mods'
QTYS = 'qtys'
NAMES = 'names'
STRIPPED_WORDS = 'stripped_words'

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
    'slice': 'ea',
    'smidgen': 'smidgen',
    'stalk': 'ea',
    'sprig': 'ea',
    'can': 'ea',
    'tin': 'ea',
    'jar': 'ea',
}

# nltk base set (english) with 't', 'with', 'or', 'to' removed
STOPWORDS = {
    'had', 'few', 'under', 'on', 'an', 'its', 'why', 'were', 'all', 'doing',
    'while', 'how', 'don', 'same', 'is', 'because', 'him', 'ourselves', 'off',
    'herself', 'has', 'into', 'd', 'out', 'he', 'against', 'themselves',
    'wouldn', 'theirs', 'be', 'above', 'up', 'own', 'are', 'when',
    'through', 'will', 'by', 'our', 'who', 'between', 'so', 'ain', 'this',
    'than', 'aren', 'them', 'not', 'wasn', 'your', 'these', 'himself', 'of',
    'down', 'won', 'for', 'only', 'as', 'myself', 'both', 'yours', 'during',
    'you', 'too', 'where', 's', 'hadn', 'about', 'and', 'been', 'very', 'do',
    'in', 'at', 'over', 'most', 'o', 'that', 'was', 'again', 'further',
    'couldn', 'having', 'hasn', 'mightn', 'me', 'no', 'her', 'hers', 'ours',
    'haven', 'my', 'it', 'nor', 'those', 'she', 'what', 'a', 're',
    'but', 'just', 'once', 'whom', 'from', 'am', 'below', 'mustn', 'ma', 've',
    'the', 'more', 'll', 'didn', 'needn', 'then', 'isn', 'should', 'his',
    'before', 'doesn', 'm', 'did', 'yourself', 'other', 'yourselves', 'can',
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
    'fine',
    'firm',
    'finely',
    'flaky',
    'fresh',  # leave this in for "fresh bean"?
    'freshly',
    'frozen',  # leave this in for "frozen pea"?
    'garnish',
    'gently',
    'halved',
    'halves',
    'hulled',
    'interval',
    'kitchen',
    'like',
    'twine',
    'large',
    'least',
    'leftover',
    'low-sodium',
    'medium',
    'mild',
    'optional',
    'peeled',
    'picked',
    'pitted',
    'plain',
    'preferably',
    'pure',
    'quartered',
    'ripe',
    'room',
    'salted',
    'scrubbed',
    'seeded',
    'serving',
    'small',
    'softened',
    'stemmed',
    'taste',
    'temperature',
    'thawed',
    'thinly',
    'trimmed',
    'unsalted',
    'unsweetened',
    'washed',
}

NO_SINGULAR = {
    'across',
    'asparagus',
    'bitters',
    'brussels',
    'couscous',
    'dice',
    'haas',
    'molasses',
    'plus',
    'schnapps',
    'slice',
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
    'freeze-dried',
    'grated',
    'ground',
    'gutted',
    'heaping',
    'jarred',
    'lengthwise',
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
    'smashed',
    'smoked',
    'squeezed',
    'steamed',
    'torn',
    'well',
    'whipped',
    'whisked',
    'zested',
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


def case_insensitize(text):
    """
    return a regex that matches the input text regardless of casing
    """
    out = ''
    for char in text.lower():
        out += '[{}{}]'.format(char, char.upper())
    return out


text_numbers = {r'(^|\W){}($|\W)'.format(case_insensitize(
    unit)): r'\g<1>{}\g<2>'.format(val) for unit, val in TEXT_NUMBERS.items()}

unit_labels = [case_insensitize(unit) for unit in UNITS]
units_group = r'|'.join(unit_labels)

# start unit regex looks for quantity-less units at the start of a string, e.g. "handful of basil"
start_unit_regex = re.compile(r'^(?P<unit>{})\s+'.format(units_group))

# "with" clauses are always unhelpful. We think.
with_clause = re.compile(r'[Ww]ith.*?[,\n\)]')
# separate this out bc it doesn't seem to work when we include $ in the terminating bit
with_term = re.compile(r'[Ww]ith.*')

# These look for numbers/fractions optionally separated by a space,
# e.g. "2.0", "1 1/2". The only requirement is the initial number (or decimal
# point)
qty_regex_1 = r'[\d\.]+[-\.\/\s]?\d*[\.\/\s]?\d*\s?'
# qty_regex_2 is identical except it's entirely optional
qty_regex_2 = r'[\d\.]*[-\.\/\s]?\d*[\.\/\s]?\d*\s?'

# multi_qty_regex looks for pairs of quantities separated by "to" or "or"
# So far, this separator works ok but it could be made more robust to caps, dashes, etc
multi_qty_regex = r'(?P<qty>{}(([Tt][Oo]|[Oo][Rr])\s)*{})'.format(
    qty_regex_1, qty_regex_2)

# OG: works pretty good
units_regex = re.compile(
    multi_qty_regex + r'(?P<qual>\s*\(.+?\)\s*)?(?P<unit>{})?(?:\s|,|$)'.format(units_group))

units_regex = re.compile(
    multi_qty_regex + r'(?P<qual>\s*\(.+?\)\s*)?(?P<unit>{})?(?P<per>\s[Ee][Aa][Cc][Hh])?(?:\s|,|$)'.format(units_group))


# hrefs
# TODO: improve this, e.g. there could be a > in the href
href_start = r'<a[^>]*>'
href_end = '</a>'


def no_singular(word):
    """ Words that should not be singularized even though they end in `s` """
    return (
        word.endswith('ss') or
        word in NO_SINGULAR or
        word.endswith('\'s')
    )


def quantify(match):
    # given a units match dict, return a dict of {'qty':float, 'unit':str, 'qualifiers': list}
    result = {'unit': 'ea', 'qty': 1, 'qualifiers': [], 'per': None}  # default
    qty = match.get('qty')
    unit = match.get('unit')
    qualifier = match.get('qual')
    per = match.get('per')
    if unit:
        # try case sensitive first due to Teaspoon/tablespoon
        result['unit'] = UNITS.get(unit, UNITS.get(unit.lower()))

    if per:
        result['per'] = match.get('per')

    if qty:
        qtys = re.split(r'[-\s]', qty)
        entry_count = 1  # accounting for 'or', 'to' ranges
        total = 0.0
        quantified = False
        for q in qtys:
            if q.lower().strip() in ['or', 'to']:
                entry_count += 1
                continue
            try:
                quantified = True
                if ('/') in q:
                    # convert fraction
                    frac = q.split('/')
                    total += float(frac[0]) / float(frac[1])
                else:
                    total += float(q)
            except ValueError:
                continue
        if quantified:
            result['qty'] = total / entry_count

    if qualifier:
        parsed_qual = match_units(qualifier)
        result['qualifiers'] = [quantify(q[2]) for q in parsed_qual]
    return result


empty_parentheses = re.compile(r'\(\s*\)')


def names_mods(text):
    # text should have stopwords removed
    text = re.sub(with_clause, '', text)
    text = re.sub(with_term, '', text)
    cleaned_text = []
    mods = []
    # TODO: should we strip out non-empty parentheticals?
    text = re.sub(empty_parentheses, '', text)

    for mismatch in [('(', ')'), (')', '(')]:
        if mismatch[0] in text and not mismatch[1] in text:
            text = text.replace(mismatch[0], '')
    for word in text.split(' '):
        word = word.lower().strip()
        if word.strip(',') in PREP_MODS:
            mods += [word.strip(',')]
            continue
        elif word in ['/']:
            continue
        elif word:
            cleaned_text += [word]
    text = ' '.join(cleaned_text)
    # split on comma, or, and
    text = re.split(r',$|,\s|\sor\s|\sor$|\sand\s|\sand$', text)
    return [r.strip() for r in text if r], mods


def pad_parentheses(text):
    """ Pad parentheses with spaces """
    return text.replace('(', '( ').replace(')', ' )')


qualifiers = r'([\d\.]+\s+\d+\/\d+-\w*)|([\d\.\/]+-+[-\w]+)'


def parenthesize_qualifiers(text):
    # parenthesize things like 4-pound or five-to-size-pounds so they get
    # treated as qualifiers
    return re.sub(qualifiers, '(\g<1>\g<2>)', text)


def devulgarize(text):
    """ Expand unicode vulgar fractions, prepending a space"""
    for k, v in VULGAR_FRACTIONS.items():
        text = text.replace(k, ' ' + v)
    return text


slashed_text_left = re.compile(r'(\D)/(\w)')
slashed_text_right = re.compile(r'(\w)/(\D)')
slashed_text_sub = '\g<1> / \g<2>'
comma_text_left = re.compile(r'(\D),(\w)')
comma_text_right = re.compile(r'(\w),(\D)')
comma_text_sub = '\g<1>, \g<2>'
hyphen_text_right = re.compile(r'(\d)-(\w)')
hyphen_text_sub = '\g<1> \g<2>'


def pad_punctuation(text):
    """
    Add space on either side of non-numeric slashes and commas, e.g.
        this/that -> this / that
        this,that -> this, that
        this/4 -> this / 4
        this,4 -> this, 4
        4/this -> 4 / this
        4,this -> 4, this
        1/4 -> 1/4
        1,4 -> 1,4

    Remove hyphens between numbers and words
    """
    for slash in [slashed_text_left, slashed_text_right]:
        text = re.sub(slash, slashed_text_sub, text)
    for comma in [comma_text_left, comma_text_right]:
        text = re.sub(comma, comma_text_sub, text)
    text = re.sub(hyphen_text_right, hyphen_text_sub, text)
    return text


def pad_ranges(text):
    """
    Replace `-` with ` ` when it's sandwiching `to`, as in
    `six-to-eight` -> `six to eight`
    """
    return re.sub(r'-[Tt][Oo]-', ' to ', text)


def strip_hrefs(text):
    text = re.sub(href_start, '', text)
    text = text.replace(href_end, '')
    return text


def numerify(text):
    """
    Repace text numbers with numbers
    """
    for match, repl in text_numbers.items():
        text = re.sub(match, repl, text)
    return text


def clean(text):
    """
    Singularize nouns and remove stopwords, returning a cleaned string
    and a list of removed stopwords.
    """
    stripped_words = []
    cleaned_words = []

    for word in re.split(r'\s', text):
        if (not word) or word.isspace():
            continue  # multiple space or whitespace

        has_comma = word.endswith(',')
        if has_comma:
            word = word[:-1]
        try:
            p.singular_noun(word)
        except Exception as err:
            logging.error(
                'Unable to singular_noun with word {}'.format(word))
            for ch in word:
                print('unicode is {}'.format(ord(ch)))
            raise err

        if word.lower().strip(',') in STOPWORDS:
            stripped_words += [word.lower()]
            continue
        if no_singular(word.lower()):
            cleaned_words += [word + ',' if has_comma else word]
        elif not p.singular_noun(word):
            cleaned_words += [word + ',' if has_comma else word]
        else:
            cleaned_words += [p.singular_noun(word) +
                              ',' if has_comma else p.singular_noun(word)]

    return ' '.join(cleaned_words), stripped_words


def match_units(text):
    def strip(groupdict):
        # remove any leading/trailing spaces (regex artifacts)
        for k, v in groupdict.items():
            groupdict[k] = v.strip() if v else v
        return groupdict
    start_match = re.match(start_unit_regex, text)
    matches = [(start_match.start(), start_match.end(), strip(
        start_match.groupdict()))] if start_match else []
    matches += [(el.start(), el.end(), strip(el.groupdict()))
                for el in re.finditer(units_regex, text)]
    return matches


def amounts(text_entry):
    """Given a text entry, return a dictionary of form
    {
        'qtys': [{'qty':float, 'unit':str},...],
        'names': [str],
        'mods': [str],
        'stripped_words': [str],
    }
    This uses a set of text transformations and regexes to extract amount
    features from the text.

    If no `text_entry` is provided, return {'error': True}.

    Note: text transformations should be isolated in functions to better
    facilitate testing.
    """

    if not text_entry:
        return {'error': True}

    # remove hrefs
    text_entry = strip_hrefs(text_entry)

    # replace numbers-as-words with digits
    text_entry = numerify(text_entry)

    # put qualifier structures in parentheses
    text_entry = parenthesize_qualifiers(text_entry)

    # add leading/trailing spaces to parentheticals
    text_entry = pad_parentheses(text_entry)

    # expand unicode vulgar fractions, prepending a space
    text_entry = devulgarize(text_entry)

    text_entry = pad_ranges(text_entry)
    # pad non-fraction slashes & commas with spaces
    text_entry = pad_punctuation(text_entry)

    # singularize nouns; remove stopwords; preserve casing for units parsing
    cleaned_text, stripped_words = clean(text_entry)

    matches = match_units(cleaned_text)
    if len(matches) == 0:
        # infer a single `ea` unit
        remainder, mods = names_mods(cleaned_text)
        return {
            QTYS: [{'qty': 1, 'unit': 'ea', 'qualifiers': [], 'per': None}],
            NAMES: remainder,
            MODS: mods,
            STRIPPED_WORDS: stripped_words,
        }

    qtys = [quantify(m[2]) for m in matches]

    remainder = re.sub(start_unit_regex, '', cleaned_text)
    remainder = re.sub(units_regex, '', remainder)
    remainder = re.sub(r'\([^\)]*\)', '', remainder)

    remainder, mods = names_mods(remainder)
    return {
        QTYS: qtys,
        NAMES: remainder,
        MODS: mods,
        STRIPPED_WORDS: stripped_words,
    }
