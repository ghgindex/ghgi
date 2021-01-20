class Convert:
    ENERGY = {
        'kcal': 4184,
        'cal': 4.184,
        'joule': 1.0,
    }

    MASS = {
        'kg': 1000.0,
        'pound': 453.592,
        'ounce': 28.3495,
        'g': 1.0,
    }

    VOLUME = {
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
        'ml': 1.0,
        'dash': 0.616,
        'pinch': 0.308,
        'smidgen': 0.154,
    }

    
    @classmethod
    def to_metric(cls, quantity, unit, specific_gravity):
        if unit in cls.VOLUME:
            quantity *= cls.VOLUME[unit]
            if specific_gravity:
                quantity *= specific_gravity
        elif unit in cls.MASS:
            quantity *= cls.MASS[unit]
        elif unit in cls.ENERGY:
            quantity *= cls.ENERGY[unit]
        return quantity
