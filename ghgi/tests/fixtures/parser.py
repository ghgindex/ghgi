"""
Parser text fixtures

Fixtures are lists of tuples of (in, out) for different tests
"""

REGEX_UNITS_DATA = [

    ('1 tablespoon plus 2 teaspoon kosher salt', [
        {'qty': '1', 'qual': None, 'unit': 'tablespoon',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
        {'qty': '2', 'qual': None, 'unit': 'teaspoon',
            'per': None, 'plus': 'plus', 'plural': None, 'mods': None}
    ]),
    ('1 ( 8-ounce / 230g ) can ( about 230g )', [
        {'qty': '1', 'qual': '( 8-ounce / 230g )',
         'unit': 'can', 'per': None, 'plus': None, 'plural': None, 'mods': None},
        {'qty': '230', 'qual': None, 'unit': 'g',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
    ('handful ( 1 cup ) stuff', [
        {'unit': 'handful', 'mods': None},
        {'qty': '1', 'qual': None, 'unit': 'cup',
            'per': None, 'plus': None, 'plural': None, 'mods': None}
    ]),
    ('1 ( 8-ounce ) stalk ( about 230g )', [
        {'qty': '1', 'qual': '( 8-ounce )', 'unit': 'stalk',
         'per': None, 'plus': None, 'plural': None, 'mods': None},
        {'qty': '230', 'qual': None, 'unit': 'g',
            'per': None, 'plus': None, 'plural': None, 'mods': None}
    ]),
    ('1 ( 8-ounce ) stalk ( about 230g )', [
        {'qty': '1', 'qual': '( 8-ounce )', 'unit': 'stalk',
         'per': None, 'plus': None, 'plural': None, 'mods': None},
        {'qty': '230', 'qual': None, 'unit': 'g',
            'per': None, 'plus': None, 'plural': None, 'mods': None}
    ]),
    ('1 ( 8-ounce ) stalk ( about 230g ) or 1 handful', [
        {'qty': '1', 'qual': '( 8-ounce )', 'unit': 'stalk',
         'per': None, 'plus': None, 'plural': None, 'mods': None},
        {'qty': '230', 'qual': None, 'unit': 'g',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
        {'qty': '1', 'qual': None, 'unit': 'handful',
            'per': None, 'plus': None, 'plural': None, 'mods': None}
    ]),
    ('1 packed cup cocoa powder', [
        {'qty': '1', 'qual': None, 'unit': 'cup',
            'per': None, 'plus': None, 'plural': None, 'mods': 'packed'},
    ]),
    ('1 large cup cocoa powder', [
        {'qty': '1', 'qual': None, 'unit': 'cup',
            'per': None, 'plus': None, 'plural': None, 'mods': 'large'},
    ]),
    ('1 tablespoon dark cocoa powder / 8 gram', [
        {'qty': '1', 'qual': None, 'unit': 'tablespoon',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
        {'qty': '8', 'qual': None, 'unit': 'gram',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
    ('185 gram all-purpose flour ( 1 1/2 cup )', [
        {'qty': '185', 'qual': None, 'unit': 'gram',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
        {'qty': '1 1/2', 'qual': None, 'unit': 'cup',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
    ('1 or 2 cup', [
        {'qty': '1 or 2', 'qual': None, 'unit': 'cup',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
    ('1 to 2 cup', [
        {'qty': '1 to 2', 'qual': None, 'unit': 'cup',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
    ('8-ounce', [
        {'qty': '8-', 'qual': None, 'unit': 'ounce',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
    ('8-ounce ', [
        {'qty': '8-', 'qual': None, 'unit': 'ounce',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
    ('8-ounces', [
        {'qty': '8-', 'qual': None, 'unit': 'ounce',
            'per': None, 'plus': None, 'plural': 's', 'mods': None},
    ]),
    ('1 cup flour', [
        {'qty': '1', 'qual': None, 'unit': 'cup',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
    ('1 cupperino flour', [
        {'qty': '1', 'qual': None, 'unit': None,
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
    ('1/2 cup flour', [
        {'qty': '1/2', 'qual': None, 'unit': 'cup',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
    ('0.5c flour', [
        {'qty': '0.5', 'qual': None, 'unit': 'c',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
    ('.5c flour', [
        {'qty': '.5', 'qual': None, 'unit': 'c',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
    ('1-1/2 cup flour', [
        {'qty': '1-1/2', 'qual': None, 'unit': 'cup',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
    ('1 cup flour 2 cup flour', [
        {'qty': '1', 'qual': None, 'unit': 'cup',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
        {'qty': '2', 'qual': None, 'unit': 'cup',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
    ('1 1/2 cup ( 2 kg ) flour', [
        {'qty': '1 1/2', 'qual': None, 'unit': 'cup',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
        {'qty': '2', 'qual': None, 'unit': 'kg',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
    ('1 cup flour 1 1/2 cup flour', [
        {'qty': '1', 'qual': None, 'unit': 'cup',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
        {'qty': '1 1/2', 'qual': None, 'unit': 'cup',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
    ('( 8-ounce )', [
        {'qty': '8-', 'qual': None, 'unit': 'ounce',
            'per': None, 'plus': None, 'plural': None, 'mods': None},
    ]),
]

AMOUNTS_DATA = [
    # 8 ounces to 1 pound smoked kielbasa, diagonally sliced 1/4-inch-thick -> we don't handle the units change
    # Oil (olive, coconut or grapeseed)
    # 2 to 3 pounds root or dense vegetable, peeled if you like and cut into 1-inch chunks or wedges (carrots, beets, potatoes, sweet potatoes, turnips, radishes, rutabaga, winter squashes)
    # Torn fresh herbs, such as mint, dill, cilantro or parsley, for serving
    ('1/2 pound fresh tuna, grilled or 6 1/2- to 7-ounce can albacore tuna, packed in water', {
        # TODO: this should capture the can as a `pkg`
        'qtys': [
            {'per': None, 'qty': 0.5, 'qualifiers': [],
                'plus': False, 'unit': 'pound'},
            {'per': None, 'qty': 6.75, 'qualifiers': [],
             'plus': False, 'unit': 'ounce'}
        ],
        'names': ['tuna', 'albacore tuna'],
        'mods': ['packed'],
        'stripped_words': ['fresh', 'grilled'],
    }),
    ('Two 5-ounce (140g) cans tuna in olive oil, drained (or 10 ounces/280g shredded roast chicken meat)', {
        'qtys': [
            {'per': None, 'qty': 2.0, 'qualifiers': [
                {'unit': 'ounce', 'qty': 5.0, 'per': 'each',
                 'qualifiers': [], 'plus': False},
                {'per': 'each', 'qty': 140.0, 'qualifiers': [],
                 'plus': False, 'unit': 'g'},
            ], 'plus': False, 'unit': 'pkg'},
            {'unit': 'ounce', 'qty': 10.0, 'qualifiers': [],
                'per': None, 'plus': False},
            {'unit': 'g', 'qty': 280.0, 'qualifiers': [], 'per': None, 'plus': False}
        ],
        'names':['tuna'],
        'mods':[],
        'stripped_words': [],
    }),
    ('2 (6-ounce) cans Italian tuna in water or oil, drained', {
        'qtys': [{'per': None, 'qty': 2.0, 'qualifiers': [
            {'unit': 'ounce', 'qty': 6.0, 'per': 'each',
             'qualifiers': [], 'plus': False}
        ], 'plus': False, 'unit': 'pkg'}],
        'names': ['italian tuna'],
        'mods': [],
        'stripped_words': [],
    }),
    ('1 (5-ounce) can tuna packed in olive oil, preferably Italian (see note)', {
        'qtys': [{'per': None, 'qty': 1.0, 'qualifiers': [
            {'unit': 'ounce', 'qty': 5.0, 'per': 'each',
             'qualifiers': [], 'plus': False}
        ], 'plus': False, 'unit': 'pkg'}],
        'names': ['tuna'],
        'mods': ['packed'],
        'stripped_words': ['preferably'],
    }),
    ('2 4-pound Atlantic salmon (2 1/4 inches at thickest point), scaled and cleaned, gills removed, head and tail on, interior cavity well washed', {
        'qtys': [
            {
                'unit': 'ea',
                'qty': 2.0,
                'per': None,
                'plus': False,
                'qualifiers': [
                    {
                        'unit': 'pound',
                        'qty': 4.0,
                        'per': 'each',
                        'plus': False,
                        'qualifiers': []
                    }
                ]
            },
            {
                'unit': 'ea',
                'qty': 2.25,
                'per': None,
                'plus': False,
                'qualifiers': []
            }
        ],
        'names': [
            'atlantic salmon',
            'gill removed',
            'head tail on',
            'interior cavity'
        ],
        'mods': [
            'scaled',
            'cleaned',
            'well'
        ],
        'stripped_words': [
            'and',
            'and',
            'washed'
        ]
    }),
    ('For the filling:', {
        'qtys': [{'per': None, 'qty': 1.0, 'qualifiers': [], 'plus': False, 'unit': 'ea'}],
        'names': [],
        'mods': [],
        'stripped_words': [],
    }),
    ('6 cups <a href="https://cooking.nytimes.com/recipes/1021916-vegan-bolognese">vegan Bolognese</a>', {
        'qtys': [{'unit': 'cup', 'qty': 6.0, 'per': None, 'plus': False, 'qualifiers': []}],
        'names': ['vegan bolognese'],
        'mods': [],
        'stripped_words': []
    }),
    ('1 packed cup cilantro, coarsely chopped', {
        'qtys': [{'unit': 'cup', 'qty': 1.0, 'per': None, 'plus': False, 'qualifiers': []}],
        'names': ['cilantro'],
        'mods': ['chopped'],
        'stripped_words': ['coarsely']
    }),
    ('4 (6-ounce) mild white fish fillets (for example, cod, hake or blackfish)', {
        'qtys': [
            {'unit': 'ea', 'qty': 4.0, 'per': None, 'plus': False, 'qualifiers': [
                {'unit': 'ounce', 'qty': 6.0, 'per': 'each',
                    'qualifiers': [], 'plus': False}
            ]}
        ],
        'names': ['white fish'],
        'mods': [],
        'stripped_words': ['mild', 'fillets', 'for']
    }),
    ('1 (10- to 14-pound) turkey', {
        'qtys': [
            {'unit': 'ea', 'qty': 1.0, 'per': None,
             'plus': False, 'qualifiers': [
                     {'unit': 'pound', 'qty': 12, 'per': 'each',
                         'qualifiers': [], 'plus': False}
             ]}
        ],
        'names': ['turkey'],
        'mods': [],
        'stripped_words': [],
    }),
    ('1 (10- to 14- pound) turkey', {
        'qtys': [
            {'unit': 'ea', 'qty': 1.0, 'per': None,
             'plus': False, 'qualifiers': [
                     {'unit': 'pound', 'qty': 12, 'per': 'each',
                         'qualifiers': [], 'plus': False}
             ]}
        ],
        'names': ['turkey'],
        'mods': [],
        'stripped_words': [],
    }),
    ('1¼ cup/80 grams plus 2 teaspoons/5 grams mild honey', {
        'qtys': [
            {'unit': 'cup', 'qty': 1.25, 'per': None,
                'plus': False, 'qualifiers': []},
            {'unit': 'g', 'qty': 80.0, 'per': None,
                'plus': False, 'qualifiers': []},
            {'unit': 'teaspoon', 'qty': 2.0, 'per': None,
                'plus': True, 'qualifiers': []},
            {'unit': 'g', 'qty': 5.0, 'per': None,
                'plus': False, 'qualifiers': []}
        ],
        'names': ['honey'],
        'mods': [],
        'stripped_words': ['mild'],
    }),
    ('1 six-to-eight-pound, cleaned, whole salmon, preferably with head left on (see note)', {
        'qtys': [
            {
                'unit': 'ea',
                'qty': 1.0,
                'per': None,
                'plus': False,
                'qualifiers': [
                    {
                        'unit': 'pound',
                        'qty': 7.0,
                        'per': 'each',
                        'qualifiers': [],
                        'plus': False,
                    }
                ]
            }
        ],
        'names': [
            'whole salmon'
        ],
        'mods': [
            'cleaned'
        ],
        'stripped_words': [
            'preferably',
        ]
    }),
    ('1 (4-ounce) can smoked mussels', {
        'qtys': [
            {
                'unit': 'pkg',
                'qty': 1.0,
                'per': None,
                'plus': False,
                'qualifiers': [
                    {
                        'unit': 'ounce',
                        'qty': 4.0,
                        'per': 'each',
                        'plus': False,
                        'qualifiers': []
                    }
                ]
            }
        ],
        'names': [
            'mussel'
        ],
        'mods': [
            'smoked'
        ],
        'stripped_words': [
        ]
    }),
    ('1 (1 1/2-pound) salmon fillet, skin-on or skinless', {
        'qtys': [
            {
                'unit': 'ea',
                'qty': 1.0,
                'per': None,
                'plus': False,
                'qualifiers': [
                    {
                        'unit': 'pound',
                        'qty': 1.5,
                        'per': 'each',
                        'plus': False,
                        'qualifiers': []
                    }
                ]
            }
        ],
        'names': [
            'salmon'
        ],
        'mods': [
            'skin-on',
            'skinless'
        ],
        'stripped_words': [
            'fillet'
        ]
    }),
    ('1 salmon about 4 1/2 pounds, boned with head and tail left on', {
        'qtys': [
            {
                'unit': 'ea',
                'qty': 1.0,
                'per': None,
                'plus': False,
                'qualifiers': []
            },
            {
                'unit': 'pound',
                'qty': 4.5,
                'per': None,
                'plus': False,
                'qualifiers': []
            }
        ],
        'names': [
            'salmon'
        ],
        'mods': [
            'boned'
        ],
        'stripped_words': [
            'about',
            'and',
        ]
    }),
    ('4 whole fish, like sea bass or black bass, 1 to 1 1/2 pounds each', {
        'qtys': [
            {
                'unit': 'ea',
                'qty': 4.0,
                'per': None,
                'plus': False,
                'qualifiers': []
            },
            {
                'unit': 'pound',
                'qty': 1.25,
                'per': 'each',
                'plus': False,
                'qualifiers': []
            }
        ],
        'names': [
            'whole fish',
            'sea bass',
            'black bass'
        ],
        'mods': [],
        'stripped_words': [
            'like',
        ]
    }),
    ('4 whole fish,, like sea bass or black bass, 1 to 1.5 pounds each', {
        'qtys': [
            {
                'unit': 'ea',
                'qty': 4.0,
                'per': None,
                'plus': False,
                'qualifiers': []
            },
            {
                'unit': 'pound',
                'qty': 1.25,
                'per': 'each',
                'plus': False,
                'qualifiers': []
            }
        ],
        'names': [
            'whole fish',
            'sea bass',
            'black bass'
        ],
        'mods': [],
        'stripped_words': [
            'like',
        ]
    }
    ),
    ('1 salmon or other firm fish, about 2 pounds, gutted and scaled, with the head left on', {
        'qtys': [
            {
                'unit': 'ea',
                'qty': 1.0,
                'per': None,
                'plus': False,
                'qualifiers': []
            },
            {
                'unit': 'pound',
                'qty': 2.0,
                'per': None,
                'plus': False,
                'qualifiers': []
            }
        ],
        'names': [
            'salmon',
            'fish'
        ],
        'mods': [
            'gutted',
            'scaled'
        ],
        'stripped_words': [
            'other',
            'firm',
            'about',
            'and',
            'the',
        ]
    }),

    ('1 scallion, chopped, for serving', {
        'qtys': [
            {'unit': 'ea', 'qty': 1, 'per': None, 'plus': False,
             'qualifiers': []}
        ],

        'names': ['scallion'],
        'mods': ['chopped'],
        'stripped_words': ['for', 'serving'],
    }),
    ('1 or 2 cup', {
        'qtys': [{'unit': 'cup', 'qty': 1.5, 'per': None, 'plus': False, 'qualifiers': []}],
        'names': [],
        'mods': [],
        'stripped_words': [],
    }),
    ('5 to 7 handful', {
        'qtys': [{'unit': 'handful', 'qty': 6, 'per': None, 'plus': False, 'qualifiers': []}],
        'names': [],
        'mods': [],
        'stripped_words': [],
    }),
    ('yada yada', {
        'qtys': [
            {'unit': 'ea', 'qty': 1, 'per': None, 'plus': False, 'qualifiers': []}
        ],
        'names': ['yada yada'],
        'mods': [],
        'stripped_words': [],
    }),
    ('chopped yada yada', {
        'qtys': [
            {'unit': 'ea', 'qty': 1, 'per': None, 'plus': False, 'qualifiers': []}
        ],
        'names': ['yada yada'],
        'mods': ['chopped'],
        'stripped_words': [],
    }),
    ('1 cup flour', {
        'qtys': [
            {'unit': 'cup', 'qty': 1.0, 'per': None,
                'plus': False, 'qualifiers': []}
        ],
        'names': ['flour'],
        'mods': [],
        'stripped_words': [],
    }),
    ('1 c flour', {
        'qtys': [
            {'unit': 'cup', 'qty': 1.0, 'per': None,
                'plus': False, 'qualifiers': []}
        ],
        'names': ['flour'],
        'mods': [],
        'stripped_words': [],
    }),
    ('1.5c flour', {
        'qtys': [
            {'unit': 'cup', 'qty': 1.5, 'per': None,
                'plus': False, 'qualifiers': []}
        ],
        'names': ['flour'],
        'mods': [],
        'stripped_words': [],
    }),
    ('1 1/2c flour', {
        'qtys': [
            {'unit': 'cup', 'qty': 1.5, 'per': None,
                'plus': False, 'qualifiers': []}
        ],
        'names': ['flour'],
        'mods': [],
        'stripped_words': [],
    }),
    ('1/4 cup/80 grams mild honey', {
        'qtys': [
            {'unit': 'cup', 'qty': 0.25, 'per': None,
                'plus': False, 'qualifiers': []},
            {'unit': 'g', 'qty': 80.0, 'per': None,
                'plus': False, 'qualifiers': []}
        ],
        'names': ['honey'],
        'mods': [],
        'stripped_words': ['mild'],
    }),
    ('1¼ cup/80 grams mild honey', {
        'qtys': [
            {'unit': 'cup', 'qty': 1.25, 'per': None,
                'plus': False, 'qualifiers': []},
            {'unit': 'g', 'qty': 80.0, 'per': None,
                'plus': False, 'qualifiers': []}
        ],
        'names': ['honey'],
        'mods': [],
        'stripped_words': ['mild'],
    }),
    ('1¼ cup (approx. 80 grams) mild honey', {
        'qtys': [
            {'unit': 'cup', 'qty': 1.25, 'per': None,
                'plus': False, 'qualifiers': []},
            {'unit': 'g', 'qty': 80.0, 'per': None,
                'plus': False, 'qualifiers': []}
        ],
        'names': ['honey'],
        'mods': [],
        'stripped_words': ['approx.', 'mild'],
    }),
    ('350g (approx. 1 1/2 cups) mild honey', {
        'qtys': [
            {'unit': 'g', 'qty': 350, 'per': None,
                'plus': False, 'qualifiers': []},
            {'unit': 'cup', 'qty': 1.5, 'per': None,
                'plus': False, 'qualifiers': []}
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
