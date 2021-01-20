from unittest import TestCase

from ghgi.convert import Convert

class TestConvert(TestCase):
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

    def test_convert(self):
        for unit, conversion in self.MASS.items():
            self.assertEqual(Convert.to_metric(1.0, unit, 1.0), conversion)
            self.assertEqual(Convert.to_metric(2.0, unit, 1.0), conversion*2)
            # sg doesn't affect mass
            self.assertEqual(Convert.to_metric(1.0, unit, 2.0), conversion)
            self.assertEqual(Convert.to_metric(1.0, unit, 0.0), conversion)

        for unit, conversion in self.ENERGY.items():
            self.assertEqual(Convert.to_metric(1.0, unit, 1.0), conversion)
            self.assertEqual(Convert.to_metric(2.0, unit, 1.0), conversion*2)
            # sg doesn't affect energy
            self.assertEqual(Convert.to_metric(1.0, unit, 2.0), conversion)
            self.assertEqual(Convert.to_metric(1.0, unit, 0.0), conversion)

        for unit, conversion in self.VOLUME.items():
            self.assertEqual(Convert.to_metric(1.0, unit, 1.0), conversion)
            self.assertEqual(Convert.to_metric(2.0, unit, 1.0), conversion*2)
            # sg does affect volume
            self.assertEqual(Convert.to_metric(2.0, unit, 2.0), conversion*2*2)
            self.assertEqual(Convert.to_metric(1.0, unit, 0.5), conversion*0.5)

        self.assertEqual(Convert.to_metric(1.0, 'fake_metric', 1.0), 1.0)
        self.assertEqual(Convert.to_metric(1.0, None, None), 1.0)
        self.assertEqual(Convert.to_metric(1.0, '', None), 1.0)
