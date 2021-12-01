""" GIN test fixtures
"""

QUERIES = [
    (
        'grape or cherry tomatoes',
        ('cherry tomato', ['tomatoes', 11], 1.0, 2, 2)
    ),
    (
        'salmon or fish',
        ('salmon', ['salmon', 4], 1.0, 1, 1)
    ),
    (
        'dried wide wheat noodle',
        ('wheat noodle', ['noodle', 10], 0.6666666666666666, 2, 4)
    ),
    (
        'parmigiano-reggiano',
        ('parmigiano-reggiano', ['cheese', 17], 1.0, 1, 1)
    ),
    (
        'parmigiano reggiano',
        ('parmigiano reggiano', ['cheese', 17], 1.0, 2, 2)
    )
]
