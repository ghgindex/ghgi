from unittest import TestCase
from unittest.mock import patch

from ghgi.product import Product, Category, Ingredient


class TestProduct(TestCase):
    def test_products_valid(self):
        # validate that all products have requisite minimal data:
        # mass, specific gravity, and category OR a super.
        for product in Product.db().values():
            if not Product.PARENTS in product:
                self.assertTrue(
                    any([cat.value in product for cat in Category]))
                self.assertTrue(Product.MASS in product)
                self.assertTrue(Product.SG in product)

    def test_sg(self):
        # logic test -> patch test in case db values change
        with patch.object(Product, '_db', {'water': {'sg': 1.0}, 'pulses': {'sg': 0.85}}):
            self.assertEqual(Product.sg(
                {Product.PARENTS: {'water': 100}}), 1.0)
            self.assertEqual(Product.sg({Product.PARENTS: {'water': 50}}), 0.5)
            self.assertEqual(Product.sg(
                {Product.PARENTS: {'water': 200}}), 2.0)
            self.assertAlmostEqual(Product.sg(
                {Product.PARENTS: {'water': 60, 'pulses': 40}}), 0.94)

    def test_g(self):
        # logic test -> patch test in case db values change
        with patch.object(Product, '_db', {'water': {'g': 250}, 'pulses': {'g': 100}}):
            self.assertEqual(Product.g({Product.PARENTS: {'water': 100}}), 250)
            self.assertEqual(Product.g({Product.PARENTS: {'water': 50}}), 125)
            self.assertEqual(Product.g({Product.PARENTS: {'water': 200}}), 500)
            self.assertAlmostEqual(Product.g(
                {Product.PARENTS: {'water': 60, 'pulses': 40}}), 190)

    def test_mass(self):
        product = {
            'ed': 1000,
            'g': 100,
            'sg': 2.0,
            'name': 'test'
        }
        ingredient = {
            Ingredient.QTYS: [{
                Ingredient.QTY: 2,
                Ingredient.UNIT: 'ea'
            }],
            Ingredient.PRODUCT: product
        }
        self.assertEqual(Product.mass(ingredient), 200)
        ingredient[Ingredient.QTYS][0] = {
            Ingredient.QTY: 200, Ingredient.UNIT: 'ml'}
        self.assertEqual(Product.mass(ingredient), 400)
        ingredient[Ingredient.QTYS][0] = {
            Ingredient.QTY: 110, Ingredient.UNIT: 'g'}
        self.assertEqual(Product.mass(ingredient), 110)

    def test_food_value(self):
        product = {'ed': 1000}
        self.assertEqual(Product.food_values(product), {'ed': (1000, True)})
        product = {'ed': 1000, 'of': 500}
        self.assertEqual(Product.food_values(product), {
                         'ed': (1000, True), 'of': (500, True)})

    def test_lookup(self):
        self.assertEqual(Product.lookup({'names': ['potato']})[
                         0]['name'], 'potatoes')
        self.assertEqual(Product.lookup({'names': ['potats']})[
                         0]['name'], 'potatoes')
        self.assertEqual(Product.lookup({'names': ['sweet potato']})[
                         0]['name'], 'potatoes')
        self.assertEqual(Product.lookup({'names': ['sweet potato']})[
                         0]['alias'], 'sweet potato')

    def test_labels(self):
        pass
        # print('sg', Product.sg(Product.get('butter')))
        # print('g', Product.g(Product.get('butter')))
        # print('mass', Product.mass({'qty': (1, 1.0), 'unit': (
        #     'ea', 1.0), 'product': Product.get('butter')}))

        # print('ghg_mean', Product.ghg_value(Origin.GHG_MEAN,
        #                                     Product.get('butter'), 'global'))

        # print('impact', Product.impact({'qty': (1, 1.0), 'unit': (
        #     'ea', 1.0), 'product': Product.get('butter')}))
