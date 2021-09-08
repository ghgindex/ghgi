"""Parser text fixtures

Fixtures are lists of tuples of (in, out) for different tests
"""

AMOUNTS_DATA = [
    ('1 cup flour', {
        'qtys': [{'unit': 'cup', 'qty': 1.0}],
        'names': ['flour'],
        'mods': [],
        'stripped_words': [],
    }),
    ('1 c flour', {
        'qtys': [{'unit': 'cup', 'qty': 1.0}],
        'names': ['flour'],
        'mods': [],
        'stripped_words': [],
    }),
    ('1.5c flour', {
        'qtys': [{'unit': 'cup', 'qty': 1.5}],
        'names': ['flour'],
        'mods': [],
        'stripped_words': [],
    }),
    ('1 1/2c flour', {
        'qtys': [{'unit': 'cup', 'qty': 1.5}],
        'names': ['flour'],
        'mods': [],
        'stripped_words': [],
    }),
    ('1 scallion, chopped, for serving', {
        'qtys': [{'unit': 'ea', 'qty': 1}],
        'names': ['scallion'],
        'mods': ['chopped'],
        'stripped_words': ['for', 'serving'],
    }),
    ('yada yada', {
        'qtys': [{'unit': 'ea', 'qty': 1}],
        'names': ['yada yada'],
        'mods': [],
        'stripped_words': [],
    }),
    ('chopped yada yada', {
        'qtys': [{'unit': 'ea', 'qty': 1}],
        'names': ['yada yada'],
        'mods': ['chopped'],
        'stripped_words': [],
    }),
    ('1/4 cup/80 grams mild honey', {
        'qtys': [{'unit': 'cup', 'qty': 0.25}, {'unit': 'g', 'qty': 80.0}],
        'names': ['honey'],
        'mods': [],
        'stripped_words': ['mild'],
    }),
    ('1¼ cup/80 grams mild honey', {
        'qtys': [{'unit': 'cup', 'qty': 1.25}, {'unit': 'g', 'qty': 80.0}],
        'names': ['honey'],
        'mods': [],
        'stripped_words': ['mild'],
    }),
    ('1¼ cup (approx. 80 grams) mild honey', {
        'qtys': [{'unit': 'cup', 'qty': 1.25}, {'unit': 'g', 'qty': 80.0}],
        'names': ['honey'],
        'mods': [],
        'stripped_words': ['approx.', 'mild'],
    })
]

PARENS_DATA = [
    ('', ''),
    ('abc def', 'abc def'),
    ('()', '(  )'),
    ('( )', '(   )'),
    ('(hi)', '( hi )'),
    ('(3)', '( 3 )'),
    ('(*)', '( * )'),
    ('(about 3 large)', '( about 3 large )'),
    ('(about 3 large', '( about 3 large'),
    ('about 3 large)', 'about 3 large )'),
]

VULGAR_DATA = [
    (u'\u00bc', ' 1/4'),
    (u'\u00bd', ' 1/2'),
    (u'\u00be', ' 3/4'),
    (u'\u2150', ' 1/7'),
    (u'\u2151', ' 1/9'),
    (u'\u2152', ' 1/10'),
    (u'\u2153', ' 1/3'),
    (u'\u2154', ' 2/3'),
    (u'\u2155', ' 1/5'),
    (u'\u2156', ' 2/5'),
    (u'\u2157', ' 3/5'),
    (u'\u2158', ' 4/5'),
    (u'\u2159', ' 1/6'),
    (u'\u215a', ' 5/6'),
    (u'\u215b', ' 1/8'),
    (u'\u215c', ' 3/8'),
    (u'\u215d', ' 5/8'),
    (u'\u215e', ' 7/8'),
    (u'\u215f', ' '),
    (u'\u2189', ' '),
    (u'1\u00bc', '1 1/4'),
    (u'a\u00bc', 'a 1/4'),
    (u'1\u00bcc', '1 1/4c'),
]

SLASH_DATA = [
    ('this/that', 'this / that'),
    ('this/4', 'this / 4'),
    ('4/this', '4 / this'),
    ('4/ this', '4 /  this'),
    ('1/4', '1/4')
]

CLEAN_DATA = [

]
