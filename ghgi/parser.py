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
}

# nltk base set (english) with 't', 'with' removed
STOPWORDS = {'had', 'few', 'under', 'on', 'an', 'its', 'why', 'were', 'all', 'doing', 'while', 'how', 'don', 'same', 'is', 'because', 'him', 'ourselves', 'off', 'herself', 'has', 'into', 'd', 'out', 'he', 'against', 'themselves', 'wouldn', 'theirs', 'be', 'above', 'each', 'up', 'own', 'are', 'when', 'through', 'will', 'by', 'our', 'who', 'between', 'so', 'ain', 'this', 'than', 'aren', 'them', 'not', 'wasn', 'your', 'these', 'himself', 'of', 'down', 'won', 'for', 'only', 'as', 'myself', 'both', 'yours', 'during', 'you', 'too', 'where', 's', 'hadn', 'about', 'and', 'been', 'very', 'do', 'in', 'at',
             'over', 'most', 'o', 'that', 'was', 'again', 'further', 'couldn', 'having', 'hasn', 'mightn', 'me', 'to', 'no', 'her', 'hers', 'ours', 'haven', 'my', 'it', 'nor', 'those', 'she', 'what', 'a', 're', 'but', 'just', 'once', 'whom', 'from', 'am', 'below', 'mustn', 'ma', 've', 'or', 'the', 'more', 'll', 'didn', 'needn', 'then', 'isn', 'should', 'his', 'before', 'doesn', 'm', 'did', 'yourself', 'other', 'yourselves', 'can', 'itself', 'any', 'being', 'i', 'here', 'some', 'which', 'we', 'such', 'there', 'weren', 'if', 'now', 'shan', 'after', 'they', 'shouldn', 'have', 'their', 'y', 'does', 'until'}
STOPWORDS |= {
    '',  # strip empty words (e.g. punctuation replacements)
    '~',
    'amount',
    'approx',
    'approximately',
    'approx.',
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
    'fresh',
    'freshly',
    'frozen',
    'garnish',
    'gently',
    'halved',
    'halves',
    'hulled',
    'interval',
    'kitchen',
    'twine',
    'large',
    'least',
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
    'boneless',
    'chopped',
    'creamed',
    'crosswise',
    'crushed',
    'dice',
    'diced',
    'dissolved',
    'freeze-dried',
    'grated',
    'ground',
    'heaping',
    'lengthwise',
    'melted',
    'minced',
    'packed',
    'pressed',
    'puree',
    'pureed',
    'roasted',
    'sauteed',
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
    'whipped',
    'whisked',
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

unit_labels = []
for i, unit in enumerate(UNITS):
    caps = ''
    for char in unit:
        caps += '[{}{}]'.format(char, char.upper())
    unit_labels += [caps]
units_regex = re.compile(
    r'([\d\.\/\s]+)({})?s?\s+(.*)'.format('|'.join(unit_labels)))

units_group = r'|'.join(unit_labels)
units_group += r'|[T]|[t]'
start_unit_regex = re.compile(r'^({})\s+'.format(units_group))
with_clause = re.compile(r'[Ww]ith.*?[,\n\)]')
# separate this out bc it doesn't seem to work when we include $ in the terminating bit
with_term = re.compile(r'[Ww]ith.*')
units_regex_2 = re.compile(
    r'([\(\d\.]+[-\.\/\s]*[tor]*\d*[\.\/\s]*?\d*\s*)({})?[\s\)]+'.format(units_group))
# TODO: improve this, e.g. there could be a > in the href
href_start = r'<a[^>]*>'
href_end = '</a>'


def no_singular(word):
    """ Identify words that should not be singularized even though they end in `s` """
    return (
        word.endswith('ss') or
        word in NO_SINGULAR or
        word.endswith('\'s')
    )


def quantify(match):
    # given a units match tuple, return a dict of {'qty':float, 'unit':str}
    result = {'unit': 'ea'}
    total = 0.0
    quantified = False  # only use the total if it was meaningful
    for entry in match:
        if entry is None:
            continue
        entry = entry.strip()
        if entry in UNITS:
            result['unit'] = UNITS[entry]
        elif entry.lower() in UNITS:
            result['unit'] = UNITS[entry.lower()]
        else:
            qtys = entry.split()
            for qty in qtys:
                fracs = qty.split('/')
                try:
                    if len(fracs) > 1:
                        total += float(fracs[0])/float(fracs[1])
                    else:
                        total += float(fracs[0])
                    quantified = True
                except ValueError:
                    continue
    result['qty'] = total if quantified else 1
    return result


empty_parentheses = re.compile(r'\(\s*\)')


def names_mods(text):
    # text should have stopwords removed
    text = re.sub(with_clause, '', text)
    text = re.sub(with_term, '', text)
    cleaned_text = []
    mods = []
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
    text = text.split(',')
    return [r.strip() for r in text if r], mods


def pad_parentheses(text):
    """ Pad parentheses with spaces """
    return text.replace('(', '( ').replace(')', ' )')


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
    """
    for slash in [slashed_text_left, slashed_text_right]:
        text = re.sub(slash, slashed_text_sub, text)
    for comma in [comma_text_left, comma_text_right]:
        text = re.sub(comma, comma_text_sub, text)
    return text


def strip_hrefs(text):
    text = re.sub(href_start, '', text)
    text = text.replace(href_end, '')
    return text


def clean(text):
    """
    Singularize nouns and remove stopwords, returning a cleaned string
    and a list of removed stopwords.
    """
    stripped_words = []
    cleaned_words = []

    for word in text.split(' '):
        if not word:
            continue  # multiple space
        if word.lower().strip(',') in STOPWORDS:
            stripped_words += [word.lower()]
            continue
        if no_singular(word.lower()):
            cleaned_words += [word]
        elif not p.singular_noun(word):
            cleaned_words += [word]
        else:
            cleaned_words += [p.singular_noun(word)]
    return ' '.join(cleaned_words), stripped_words


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

    # add leading/trailing spaces to parentheticals
    text_entry = pad_parentheses(text_entry)

    # expand unicode vulgar fractions, prepending a space
    text_entry = devulgarize(text_entry)

    # pad non-fraction slashes & commas with spaces
    text_entry = pad_punctuation(text_entry)

    # singularize nouns; remove stopwords; preserve casing for units parsing
    cleaned_text, stripped_words = clean(text_entry)

    start_match = re.match(start_unit_regex, cleaned_text)
    matches = [(start_match.group(), None)] if start_match else []
    matches += re.findall(units_regex_2, cleaned_text)
    if len(matches) == 0:
        # infer a single `ea` unit
        remainder, mods = names_mods(cleaned_text)
        return {
            QTYS: [{'qty': 1, 'unit': 'ea'}],
            NAMES: remainder,
            MODS: mods,
            STRIPPED_WORDS: stripped_words,
        }

    qtys = [quantify(m) for m in matches]

    remainder = re.sub(start_unit_regex, '', cleaned_text)
    remainder = re.sub(units_regex_2, '', remainder)

    remainder, mods = names_mods(remainder)
    return {
        QTYS: qtys,
        NAMES: remainder,
        MODS: mods,
        STRIPPED_WORDS: stripped_words,
    }
