"""Parser text fixtures

Fixtures are lists of tuples of (in, out) for different tests
"""
REGEX_UNITS_DATA = [
    ('1 ( 8-ounce / 230g ) can ( about 230g )', [
        {'qty': '1', 'qual': '( 8-ounce / 230g )', 'unit': 'can'},
        {'qty': '230', 'qual': None, 'unit': 'g'},
    ]),
    ('handful ( 1 cup ) stuff', [
        {'unit': 'handful'},
        {'qty': '1', 'qual': None, 'unit': 'cup'}
    ]),
    ('1 ( 8-ounce ) stalk ( about 230g )', [
        {'qty': '1', 'qual': '( 8-ounce )', 'unit': 'stalk'},
        {'qty': '230', 'qual': None, 'unit': 'g'}
    ]),
    ('1 ( 8-ounce ) stalk ( about 230g ) or 1 handful', [
        {'qty': '1', 'qual': '( 8-ounce )', 'unit': 'stalk'},
        {'qty': '230', 'qual': None, 'unit': 'g'},
        {'qty': '1', 'qual': None, 'unit': 'handful'}
    ]),
    ('1 tablespoon dark cocoa powder / 8 gram', [
        {'qty': '1', 'qual': None, 'unit': 'tablespoon'},
        {'qty': '8', 'qual': None, 'unit': 'gram'},
    ]),
    ('185 gram all-purpose flour ( 1 1/2 cup )', [
        {'qty': '185', 'qual': None, 'unit': 'gram'},
        {'qty': '1 1/2', 'qual': None, 'unit': 'cup'},
    ]),
    ('1 or 2 cup', [
        {'qty': '1 or 2', 'qual': None, 'unit': 'cup'},
    ]),
    ('1 to 2 cup', [
        {'qty': '1 to 2', 'qual': None, 'unit': 'cup'},
    ]),
    ('8-ounce', [
        {'qty': '8-', 'qual': None, 'unit': 'ounce'},
    ]),
    ('8-ounce ', [
        {'qty': '8-', 'qual': None, 'unit': 'ounce'},
    ]),
    ('1 cup flour', [
        {'qty': '1', 'qual': None, 'unit': 'cup'},
    ]),
    ('1 cupperino flour', [
        {'qty': '1', 'qual': None, 'unit': None},
    ]),
    ('1/2 cup flour', [
        {'qty': '1/2', 'qual': None, 'unit': 'cup'},
    ]),
    ('0.5c flour', [
        {'qty': '0.5', 'qual': None, 'unit': 'c'},
    ]),
    ('.5c flour', [
        {'qty': '.5', 'qual': None, 'unit': 'c'},
    ]),
    ('1-1/2 cup flour', [
        {'qty': '1-1/2', 'qual': None, 'unit': 'cup'},
    ]),
    ('1 cup flour 2 cup flour', [
        {'qty': '1', 'qual': None, 'unit': 'cup'},
        {'qty': '2', 'qual': None, 'unit': 'cup'},
    ]),
    ('1 1/2 cup ( 2 kg ) flour', [
        {'qty': '1 1/2', 'qual': None, 'unit': 'cup'},
        {'qty': '2', 'qual': None, 'unit': 'kg'},
    ]),
    ('1 cup flour 1 1/2 cup flour', [
        {'qty': '1', 'qual': None, 'unit': 'cup'},
        {'qty': '1 1/2', 'qual': None, 'unit': 'cup'},
    ]),
    ('( 8-ounce )', [
        {'qty': '8-', 'qual': None, 'unit': 'ounce'},
    ]),
]

AMOUNTS_DATA = [
    ('1 salmon about 4 1/2 pounds, boned with head and tail left on', {
        "qtys": [
            {
                "unit": "ea",
                "qty": 1.0,
                "qualifiers": []
            },
            {
                "unit": "pound",
                "qty": 4.5,
                "qualifiers": []
            }
        ],
        "names": [
            "salmon"
        ],
        "mods": [
            "boned"
        ],
        "stripped_words": [
            "about",
            "and",
            "on"
        ]
    }),
    ('4 whole fish, like sea bass or black bass, 1 to 1 1/2 pounds each', {
        "qtys": [
            {
                "unit": "ea",
                "qty": 4.0,
                "qualifiers": []
            },
            {
                "unit": "pound",
                "qty": 1.25,
                "qualifiers": []
            }
        ],
        "names": [
            "whole fish",
            "sea bass",
            "black bass"
        ],
        "mods": [],
        "stripped_words": [
            "like",
            "each"
        ]
    }),
    ('4 whole fish, like sea bass or black bass, 1 to 1.5 pounds each', {
        "qtys": [
            {
                "unit": "ea",
                "qty": 4.0,
                "qualifiers": []
            },
            {
                "unit": "pound",
                "qty": 1.25,
                "qualifiers": []
            }
        ],
        "names": [
            "whole fish",
            "sea bass",
            "black bass"
        ],
        "mods": [],
        "stripped_words": [
            "like",
            "each"
        ]
    }
    ),
    ('1 salmon or other firm fish, about 2 pounds, gutted and scaled, with the head left on', {
        "qtys": [
            {
                "unit": "ea",
                "qty": 1.0,
                "qualifiers": []
            },
            {
                "unit": "pound",
                "qty": 2.0,
                "qualifiers": []
            }
        ],
        "names": [
            "salmon",
            "fish"
        ],
        "mods": [
            "gutted",
            "scaled"
        ],
        "stripped_words": [
            "other",
            "firm",
            "about",
            "and",
            "the",
            "on"
        ]
    }),
    ('1 4-pound Atlantic salmon (2 1/4 inches at thickest point), scaled and cleaned, gills removed, head and tail on, interior cavity well washed', {
        "qtys": [
            {
                "unit": "ea",
                "qty": 1.0,
                "qualifiers": [
                    {
                        "unit": "pound",
                        "qty": 4.0,
                        "qualifiers": []
                    }
                ]
            },
            {
                "unit": "ea",
                "qty": 2.25,
                "qualifiers": []
            }
        ],
        "names": [
            "atlantic salmon",
            "gill removed",
            "head tail interior cavity"
        ],
        "mods": [
            "scaled",
            "cleaned",
            "well"
        ],
        "stripped_words": [
            "at",
            "and",
            "and",
            "on",
            "washed"
        ]
    }),
    ('1 six-to-eight-pound, cleaned, whole salmon, preferably with head left on (see note)', {
        "qtys": [
            {
                "unit": "ea",
                "qty": 1.0,
                "qualifiers": [
                    {
                        "unit": "pound",
                        "qty": 7.0,
                        "qualifiers": []
                    }
                ]
            }
        ],
        "names": [
            "whole salmon"
        ],
        "mods": [
            "cleaned"
        ],
        "stripped_words": [
            "preferably",
            "on"
        ]
    }),
    ('1 scallion, chopped, for serving', {
        'qtys': [
            {'unit': 'ea', 'qty': 1, 'qualifiers': []}
        ],
        'names': ['scallion'],
        'mods': ['chopped'],
        'stripped_words': ['for', 'serving'],
    }),
    ('1 or 2 cup', {
        'qtys': [{'unit': 'cup', 'qty': 1.5, 'qualifiers': []}],
        'names': [],
        'mods': [],
        'stripped_words': [],
    }),
    ('5 to 7 handful', {
        'qtys': [{'unit': 'handful', 'qty': 6, 'qualifiers': []}],
        'names': [],
        'mods': [],
        'stripped_words': [],
    }),
    ('yada yada', {
        'qtys': [
            {'unit': 'ea', 'qty': 1, 'qualifiers': []}
        ],
        'names': ['yada yada'],
        'mods': [],
        'stripped_words': [],
    }),
    ('chopped yada yada', {
        'qtys': [
            {'unit': 'ea', 'qty': 1, 'qualifiers': []}
        ],
        'names': ['yada yada'],
        'mods': ['chopped'],
        'stripped_words': [],
    }),
    ('1 cup flour', {
        'qtys': [
            {'unit': 'cup', 'qty': 1.0, 'qualifiers': []}
        ],
        'names': ['flour'],
        'mods': [],
        'stripped_words': [],
    }),
    ('1 c flour', {
        'qtys': [
            {'unit': 'cup', 'qty': 1.0, 'qualifiers': []}
        ],
        'names': ['flour'],
        'mods': [],
        'stripped_words': [],
    }),
    ('1.5c flour', {
        'qtys': [
            {'unit': 'cup', 'qty': 1.5, 'qualifiers': []}
        ],
        'names': ['flour'],
        'mods': [],
        'stripped_words': [],
    }),
    ('1 1/2c flour', {
        'qtys': [
            {'unit': 'cup', 'qty': 1.5, 'qualifiers': []}
        ],
        'names': ['flour'],
        'mods': [],
        'stripped_words': [],
    }),
    ('1/4 cup/80 grams mild honey', {
        'qtys': [
            {'unit': 'cup', 'qty': 0.25, 'qualifiers': []},
            {'unit': 'g', 'qty': 80.0, 'qualifiers': []}
        ],
        'names': ['honey'],
        'mods': [],
        'stripped_words': ['mild'],
    }),
    ('1¼ cup/80 grams mild honey', {
        'qtys': [
            {'unit': 'cup', 'qty': 1.25, 'qualifiers': []},
            {'unit': 'g', 'qty': 80.0, 'qualifiers': []}
        ],
        'names': ['honey'],
        'mods': [],
        'stripped_words': ['mild'],
    }),
    ('1¼ cup (approx. 80 grams) mild honey', {
        'qtys': [
            {'unit': 'cup', 'qty': 1.25, 'qualifiers': []},
            {'unit': 'g', 'qty': 80.0, 'qualifiers': []}
        ],
        'names': ['honey'],
        'mods': [],
        'stripped_words': ['approx.', 'mild'],
    }),
    ('350g (approx. 1 1/2 cups) mild honey', {
        'qtys': [
            {'unit': 'g', 'qty': 350, 'qualifiers': []},
            {'unit': 'cup', 'qty': 1.5, 'qualifiers': []}
        ],
        'names': ['honey'],
        'mods': [],
        'stripped_words': ['approx.', 'mild'],
    }),
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
