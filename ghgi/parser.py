#!/usr/bin/env python3

import re
import logging
import inflect
p = inflect.engine()

logging.basicConfig(level=logging.INFO)

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
    'stalk': 'ea',
    'sprig': 'ea',
}

# nltk base set (english) with 't', 'with' removed
STOPWORDS = {'had', 'few', 'under', 'on', 'an', 'its', 'why', 'were', 'all', 'doing', 'while', 'how', 'don', 'same', 'is', 'because', 'him', 'ourselves', 'off', 'herself', 'has', 'into', 'd', 'out', 'he', 'against', 'themselves', 'wouldn', 'theirs', 'be', 'above', 'each', 'up', 'own', 'are', 'when', 'through', 'will', 'by', 'our', 'who', 'between', 'so', 'ain', 'this', 'than', 'aren', 'them', 'not', 'wasn', 'your', 'these', 'himself', 'of', 'down', 'won', 'for', 'only', 'as', 'myself', 'both', 'yours', 'during', 'you', 'too', 'where', 's', 'hadn', 'about', 'and', 'been', 'very', 'do', 'in', 'at',
             'over', 'most', 'o', 'that', 'was', 'again', 'further', 'couldn', 'having', 'hasn', 'mightn', 'me', 'to', 'no', 'her', 'hers', 'ours', 'haven', 'my', 'it', 'nor', 'those', 'she', 'what', 'a', 're', 'but', 'just', 'once', 'whom', 'from', 'am', 'below', 'mustn', 'ma', 've', 'or', 'the', 'more', 'll', 'didn', 'needn', 'then', 'isn', 'should', 'his', 'before', 'doesn', 'm', 'did', 'yourself', 'other', 'yourselves', 'can', 'itself', 'any', 'being', 'i', 'here', 'some', 'which', 'we', 'such', 'there', 'weren', 'if', 'now', 'shan', 'after', 'they', 'shouldn', 'have', 'their', 'y', 'does', 'until'}
STOPWORDS |= {
    '', # why is this here?
    'amount',
    'baby',
    'coarse',
    'coarsely',
    'cooled',
    'cored',
    'cut',
    'desired',
    'equal',
    'fillet',
    'fine',
    'firm',
    'finely',
    'flaky',
    'fresh',
    'freshly',
    'frozen',
    'halved',
    'halves',
    'hulled',
    'interval',
    'kitchen',
    'twine',
    'large',
    'least',
    'medium',
    'optional',
    'peeled',
    'picked',
    'pitted',
    'plain',
    'quartered',
    'ripe',
    'room',
    'temperature',
    'small',
    'stemmed',
    'taste',
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
    'chopped',
    'crushed',
    'dice',
    'diced',
    'dissolved',
    'grated',
    'ground',
    'minced',
    'puree',
    'pureed',
    'sifted',
    'sliced',
    'smoked',
    'squeezed',
    'whisked',
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
start_unit_regex = re.compile(r'({})\s+'.format(units_group))
with_clause = re.compile(r'[Ww]ith.*?[,\n\)]')
# separate this out bc it doesn't seem to work when we include $ in the terminating bit
with_term = re.compile(r'[Ww]ith.*')
units_regex_2 = re.compile(
    r'([\(\d\.]+[-\.\/\s]*[tor]*\d*[\.\/\s]*?\d*\s*)({})?[\s\)]+'.format(units_group))
empty_parentheses = re.compile(r'\(\s*\)')
left_parenthesis = re.compile(r'\(')
right_parenthesis = re.compile(r'\)')


def no_singular(word):
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


def names_mods(text):
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
        if word in STOPWORDS:
            continue  # exclude
        elif word in PREP_MODS:
            mods += [word]
            continue
        elif word:
            cleaned_text += [word]
    text = ' '.join(cleaned_text)
    text = text.split(',')
    return [r.strip() for r in text if r], mods


def amounts(text_entry):
    """Given a text entry, return a dictionary of form
    {
        'qtys': [{'qty':float, 'unit':str},...],
        'names': [str],
        'mods': [str],
    }
    This uses a set of regexes to extract amount features from the text.

    If no `text_entry` is provided, return {'error': True}
    """

    if not text_entry:
        return {'error': True}
    cleaned_text = []
    text_entry = re.sub(left_parenthesis, '( ', text_entry)
    text_entry = re.sub(right_parenthesis, ' )', text_entry)
    # singularize all nouns; preserve casing for units parsing
    for word in text_entry.split(' '):
        if not word:
            continue  # multiple space
        if word.lower().strip(',') in STOPWORDS:
            continue
        if no_singular(word.lower()):
            singular = word
        else:
            singular = p.singular_noun(word)
        cleaned_text += [singular] if singular else [word]
    singularized_entry = ' '.join(cleaned_text)
    matches = re.findall(units_regex_2, singularized_entry)
    start_unit = False
    if len(matches) < 1:
        matches = re.match(start_unit_regex, singularized_entry)
        if matches:
            matches = [(matches.group(), None)]
            start_unit = True
        else:
            remainder, mods = names_mods(singularized_entry)
            return {
                'qtys': [{'qty': 1, 'unit': 'ea'}],
                'names': remainder,
                'mods': mods
            }

    qtys = [quantify(m) for m in matches]

    if start_unit:
        remainder = re.sub(start_unit_regex, '', singularized_entry)
    else:
        remainder = re.sub(units_regex_2, '', singularized_entry)

    remainder, mods = names_mods(remainder)
    return {
        'qtys': qtys,
        'names': remainder,
        'mods': mods,
    }