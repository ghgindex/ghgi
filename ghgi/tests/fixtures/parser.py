"""
Parser text fixtures

Fixtures are lists of tuples of (in, out) for different tests
"""

{'qtys': [{'qty': 236.588, 'unit': 'ml'}],
    'names': ['cocoa powder'], 'mods': ['packed']}
{'qtys': [{'qty': 236.588, 'unit': 'ml'}],
    'names': ['cocoa powder'], 'mods': ['large']}
{'qtys': [{'qty': 14.7868, 'unit': 'ml'}], 'names': [
    'dark cocoa powder / 8.0 g'], 'mods': []}
{'qtys': [{'qty': 185.0, 'unit': 'g'}], 'names': [
    'all-purpose flour 354.882 ml'], 'mods': []}
{'qtys': [{'qty': 354.882, 'unit': 'ml'}], 'names': [], 'mods': []}
{'qtys': [{'qty': 354.882, 'unit': 'ml'}], 'names': [], 'mods': []}
{'qtys': [{'qty': 226.796, 'unit': 'g'}], 'names': [], 'mods': []}
{'qtys': [{'qty': 226.796, 'unit': 'g'}], 'names': [], 'mods': []}
{'qtys': [{'qty': 226.796, 'unit': 'g'}], 'names': [], 'mods': []}
{'qtys': [{'qty': 236.588, 'unit': 'ml'}], 'names': ['flour'], 'mods': []}
{'qtys': [{'qty': 1.0, 'unit': 'ea'}],
    'names': ['cupperino flour'], 'mods': []}
{'qtys': [{'qty': 118.294, 'unit': 'ml'}], 'names': ['flour'], 'mods': []}
{'qtys': [{'qty': 118.294, 'unit': 'ml'}], 'names': ['flour'], 'mods': []}
{'qtys': [{'qty': 118.294, 'unit': 'ml'}], 'names': ['flour'], 'mods': []}
{'qtys': [{'qty': 354.882, 'unit': 'ml'}], 'names': ['flour'], 'mods': []}
{'qtys': [{'qty': 236.588, 'unit': 'ml'}],
    'names': ['flour 473.176 ml flour'], 'mods': []}
{'qtys': [{'qty': 2000.0, 'unit': 'g'}], 'names': ['flour'], 'mods': []}
{'qtys': [{'qty': 236.588, 'unit': 'ml'}],
    'names': ['flour 354.882 ml flour'], 'mods': []}

REGEX_UNITS_DATA = [

    ('1 tablespoon plus 2 teaspoon kosher salt',
     {'qtys': [{'qty': 24.64464, 'unit': 'ml'}],
      'names': ['kosher salt'], 'mods': []}
     ),
    ('1 ( 8-ounce / 230g ) can ( about 230g )',
     {'qtys': [{'qty': 226.796, 'unit': 'g'}], 'names': [], 'mods': []}
     ),
    (
        'handful ( 1 cup ) stuff',
        {'qtys': [
            {'qty': 118.0, 'unit': 'ml'},
            {'qty': 236.588, 'unit': 'ml'}
        ], 'names': ['stuff'], 'mods': []}
    ),
    (
        '1 ( 8-ounce ) stalk ( about 230g )',
        {'qtys': [{'qty': 226.796, 'unit': 'g'}], 'names': [], 'mods': []}
    ),
]

AMOUNTS_DATA = [
    # 8 ounces to 1 pound smoked kielbasa, diagonally sliced 1/4-inch-thick -> we don't handle the units change
    # TODO: would be ideal to note which units pertain to which names (based on positions in the text)
    # 4-5 ears of corn, husked [this is getting parsed as 9]
    # Oil (olive, coconut or grapeseed)
    # 2-inch slice :-| probably this just wants to become an `ea` if it doesn't already
    # '1 1/2-ounce package dried morels, or 6 ounces fresh morels plus 1/2 cup beef broth'
    # 2 to 3 pounds root or dense vegetable, peeled if you like and cut into 1-inch chunks or wedges (carrots, beets, potatoes, sweet potatoes, turnips, radishes, rutabaga, winter squashes)
    # Torn fresh herbs, such as mint, dill, cilantro or parsley, for serving
    (
        '1 (5- to 6-ounce) can or jar tuna, drained and flaked, or 1 (13-ounce) can chickpeas or white beans, drained',
        {'qtys': [{'qty': 155.92225, 'unit': 'g'}],
            'names': ['tuna'], 'mods': ['drained', 'flaked']}
    ),
    (
        '1/2 pound fresh tuna, grilled or 6 1/2- to 7-ounce can albacore tuna, packed in water',
        {'qtys': [{'qty': 226.796, 'unit': 'g'}],
            'names': ['tuna'], 'mods': []}
    ),
    (
        'Two 5-ounce (140g) cans tuna in olive oil, drained (or 10 ounces/280g shredded roast chicken meat)',
        {'qtys': [{'qty': 283.495, 'unit': 'g'}],
            'names': ['tuna'], 'mods': ['drained']}
    ),
    (
        '2 (6-ounce) cans Italian tuna in water or oil, drained',
        {'qtys': [{'qty': 340.19399999999996, 'unit': 'g'}],
         'names': ['Italian tuna'], 'mods': ['drained']}
    ),
    (
        '1 (5-ounce) can tuna packed in olive oil, preferably Italian (see note)',
        {'qtys': [{'qty': 141.7475, 'unit': 'g'}],
            'names': ['tuna'], 'mods': ['packed']}
    ),
    (
        '2 4-pound Atlantic salmon (2 1/4 inches at thickest point), scaled and cleaned, gills removed, head and tail on, interior cavity well washed',
        {'qtys': [{'qty': 3628.736, 'unit': 'g'}],
         'names': ['Atlantic salmon'], 'mods': ['well', 'scaled', 'cleaned']}
    ),
    (
        'For the filling:',
        {}
    ),
    (
        '6 cups <a href="https://cooking.nytimes.com/recipes/1021916-vegan-bolognese">vegan Bolognese</a>',
        {'qtys': [{'qty': 1419.528, 'unit': 'ml'}],
         'names': ['vegan Bolognese'], 'mods': []}
    ),
    (
        '1 packed cup cilantro, coarsely chopped',
        {'qtys': [{'qty': 236.588, 'unit': 'ml'}],
         'names': ['cilantro'], 'mods': ['chopped', 'packed']}
    ),
    (
        '4 (6-ounce) mild white fish fillets (for example, cod, hake or blackfish)',
        {'qtys': [{'qty': 680.3879999999999, 'unit': 'g'}],
         'names': ['white fish'], 'mods': []}
    ),
    (
        '1 (10- to 14-pound) turkey',
        {'qtys': [{'qty': 5443.103999999999, 'unit': 'g'}],
         'names': ['turkey'], 'mods': []}
    ),
    (
        '1 (10- to 14- pound) turkey',
        {'qtys': [{'qty': 5443.103999999999, 'unit': 'g'}],
         'names': ['turkey'], 'mods': []}
    ),
    (
        '1¼ cup/80 grams plus 2 teaspoons/5 grams mild honey',
        {'qtys': [{'qty': 85.0, 'unit': 'g'}], 'names': ['honey'], 'mods': []}
    ),
    (
        '1 six-to-eight-pound, cleaned, whole salmon, preferably with head left on (see note)',
        {'qtys': [{'qty': 3175.144, 'unit': 'g'}],
         'names': ['whole salmon'], 'mods': ['cleaned']}
    ),
    (
        '1 (4-ounce) can smoked mussels',
        {'qtys': [{'qty': 113.398, 'unit': 'g'}],
         'names': ['mussels'], 'mods': ['smoked']}
    ),
    (
        '1 (1 1/2-pound) salmon fillet, skin-on or skinless',
        {'qtys': [{'qty': 680.3879999999999, 'unit': 'g'}],
         'names': ['salmon'], 'mods': ['skin-on', 'skinless']}
    ),
    (
        '1 salmon about 4 1/2 pounds, boned with head and tail left on',
        {'qtys': [{'qty': 2041.164, 'unit': 'g'}],
            'names': ['salmon'], 'mods': ['boned']}
    ),
    (
        '4 whole fish, like sea bass or black bass, 1 to 1 1/2 pounds each',
        {'qtys': [{'qty': 2267.96, 'unit': 'g'}],
         'names': ['whole fish'], 'mods': []}
    ),
    (
        '4 whole fish,, like sea bass or black bass, 1 to 1.5 pounds each',
        {'qtys': [{'qty': 2267.96, 'unit': 'g'}],
         'names': ['whole fish'], 'mods': []}
    ),
    (
        '1 salmon or other firm fish, about 2 pounds, gutted and scaled, with the head left on',
        {'qtys': [{'qty': 907.184, 'unit': 'g'}],
         'names': ['salmon or fish'], 'mods': ['gutted', 'scaled']}
    ),
    (
        '1 scallion, chopped, for serving',
        {'qtys': [{'qty': 1.0, 'unit': 'ea'}],
            'names': ['scallion'], 'mods': ['chopped']}
    ),
    (
        '1 or 2 cup',
        {'qtys': [{'qty': 354.882, 'unit': 'ml'}], 'names': [], 'mods': []}
    ),
    (
        '5 to 7 handful',
        {'qtys': [{'qty': 708.0, 'unit': 'ml'}], 'names': [], 'mods': []}
    ),
    (
        'yada yada',
        {'qtys': [{'qty': 1.0, 'unit': 'ea'}],
            'names': ['yada yada'], 'mods': []}
    ),
    (
        'chopped yada yada',
        {'qtys': [{'qty': 1.0, 'unit': 'ea'}],
         'names': ['yada yada'], 'mods': ['chopped']}
    ),
    (
        '1 cup flour',
        {'qtys': [{'qty': 236.588, 'unit': 'ml'}],
            'names': ['flour'], 'mods': []}
    ),
    (
        '1 c flour',
        {'qtys': [{'qty': 236.588, 'unit': 'ml'}],
            'names': ['flour'], 'mods': []}
    ),
    (
        '1.5c flour',
        {'qtys': [{'qty': 354.882, 'unit': 'ml'}],
            'names': ['flour'], 'mods': []}
    ),
    (
        '1 1/2c flour',
        {'qtys': [{'qty': 354.882, 'unit': 'ml'}],
            'names': ['flour'], 'mods': []}
    ),
    (
        '1/4 cup/80 grams mild honey',
        {'qtys': [{'qty': 80.0, 'unit': 'g'}], 'names': ['honey'], 'mods': []}
    ),
    (
        '1¼ cup/80 grams mild honey',
        {'qtys': [{'qty': 80.0, 'unit': 'g'}], 'names': ['honey'], 'mods': []}
    ),
    (
        '1¼ cup (approx. 80 grams) mild honey',
        {'qtys': [{'qty': 80.0, 'unit': 'g'}], 'names': ['honey'], 'mods': []}
    ),
    (
        '350g (approx. 1 1/2 cups) mild honey',
        {'qtys': [{'qty': 350.0, 'unit': 'g'}], 'names': ['honey'], 'mods': []}
    ),
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
