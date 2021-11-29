""" GIN test fixtures
"""

QUERIES = [
    # (
    #     'grape or cherry tomatoes',
    #     (None, None, None)
    # ),
    # (
    #     'salmon or fish',
    #     (None, None, None)
    # ),
    (
        'dried wide wheat noodle',
        ('wheat noodle', ['noodle', 10], 0.6666666666666666)
    ),
    (
        'parmigiano-reggiano',
        ('parmigiano-reggiano', ['cheese', 17], 1.0)
    ),
    (
        'parmigiano reggiano',
        ('parmigiano reggiano', ['cheese', 17], 1.0)
    )
]
