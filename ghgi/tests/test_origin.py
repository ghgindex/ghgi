from unittest import TestCase

from ghgi.origin import Origin
from ghgi.reference import Reference


class TestOrigin(TestCase):
    def test_origins_meta(self):
        # make sure all origins are present
        self.assertEqual(len(Origin.ORIGINS), 4)
        self.assertTrue(all([
            origin in Origin.ORIGINS for origin in [
                'global',
                'north_america',
                'canada',
                'usa'
            ]
        ]))

    def test_origin_entries(self):
        """ Test Origin integrity: 
        If we aggregate all products across all Origins, every one of those
        products should be available in every Origin, because all products
        in sub-origins must also exist in their supers, which eventually leads
        to the global origin.
        """
        super_products = set()
        for origin in Origin.ORIGINS:
            Origin.load(origin)
            super_products |= set(Origin._db[origin].keys())
        super_products.remove('super')
        for origin in Origin.ORIGINS:
            for product in super_products:
                if product.startswith('_'):
                    continue
                values = Origin.values(origin, product)
                self.assertNotEqual(values, None)
                self.assertTrue(str(values[0]) in Reference.db())
                self.assertEqual(len(values[1]), 4)
