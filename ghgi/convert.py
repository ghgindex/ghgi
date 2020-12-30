class Convert:
    G = {
        'kg': 1000.0,
        'pound': 453.592,
        'ounce': 28.3495,
    }

    ML = {
        'gallon': 3785.41,
        'l': 1000.0,
        'quart': 946.353,
        'pint': 473.176,
        'cup': 236.588,
        'handful': 118.0,
        'fistful': 59.0,
        'fluid_oz': 29.5735,
        'tablespoon': 14.7868,
        'teaspoon': 4.92892,
        'dash': 0.616,
        'pinch': 0.308,
        'smidgen': 0.154,
    }

    JOULE = {
        'kcal': 4184,
        'cal': 4.184
    }

    @classmethod
    def convert(cls, qty, unit, sg):
        if unit in cls.ML:
            qty *= cls.ML[unit]
            if sg:
                qty *= sg
        elif unit in cls.G:
            qty *= cls.G[unit]
        elif unit in cls.JOULE:
            qty *= cls.JOULE[unit]
        return qty
