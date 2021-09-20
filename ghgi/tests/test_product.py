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
            'name': 'test',
            'super': {},
        }
        ingredient = {
            Ingredient.QTYS: [{
                Ingredient.QTY: 2,
                Ingredient.UNIT: 'ea',
                Ingredient.PER: None,
                Ingredient.QUALIFIERS: [],
            }],
            Ingredient.PRODUCT: product
        }
        self.assertEqual(Product.mass(ingredient), 200)

        ingredient[Ingredient.QTYS][0] = {
            Ingredient.QTY: 200, Ingredient.UNIT: 'ml', Ingredient.PER: None}
        self.assertEqual(Product.mass(ingredient), 400)

        ingredient[Ingredient.QTYS][0] = {
            Ingredient.QTY: 110, Ingredient.UNIT: 'g', Ingredient.PER: None}
        self.assertEqual(Product.mass(ingredient), 110)

        ingredient[Ingredient.QTYS][0] = {
            Ingredient.QTY: 2, Ingredient.UNIT: 'pkg', Ingredient.PER: None}
        self.assertEqual(Product.mass(ingredient), 2160)

        product['pkg'] = 125
        self.assertEqual(Product.mass(ingredient), 500)

        ingredient[Ingredient.QTYS][0] = {
            Ingredient.QTY: 2, Ingredient.UNIT: 'bunch', Ingredient.PER: None}
        self.assertEqual(Product.mass(ingredient), 1200)

        product['bunch'] = 10
        self.assertEqual(Product.mass(ingredient), 2000)

        del product['pkg']
        del product['bunch']
        product[Product.PARENTS] = {'parent': 100}
        with patch.object(Product, '_db', {'parent': {'pkg': 800, 'bunch': 8}, }):
            ingredient[Ingredient.QTYS][0] = {
                Ingredient.QTY: 2, Ingredient.UNIT: 'bunch', Ingredient.PER: None}
            self.assertEqual(Product.mass(ingredient), 1600)

            ingredient[Ingredient.QTYS][0] = {
                Ingredient.QTY: 2, Ingredient.UNIT: 'pkg', Ingredient.PER: None}
            self.assertEqual(Product.mass(ingredient), 3200)

    def test_qualifiers(self):
        product = {
            'ed': 1000,
            'g': 100,
            'sg': 2.0,
            'name': 'test'
        }
        ingredient = {
            Ingredient.QTYS: [{
                Ingredient.QTY: 2,
                Ingredient.UNIT: 'ea',
                Ingredient.PER: None,
                Ingredient.QUALIFIERS: [{
                    Ingredient.QTY: 512,
                    Ingredient.UNIT: 'g',
                    Ingredient.PER: 'each',
                }],
            }],
            Ingredient.PRODUCT: product
        }
        self.assertEqual(Product.mass(ingredient), 1024)

        ingredient = {
            Ingredient.QTYS: [{
                Ingredient.QTY: 2,
                Ingredient.UNIT: 'ea',
                Ingredient.PER: None,
                Ingredient.QUALIFIERS: [{
                    Ingredient.QTY: 4,
                    Ingredient.UNIT: 'ea',
                    Ingredient.PER: None,
                }],
            }],
            Ingredient.PRODUCT: product
        }
        self.assertEqual(Product.mass(ingredient), 200)

        ingredient = {
            Ingredient.QTYS: [{
                Ingredient.QTY: 2,
                Ingredient.UNIT: 'ea',
                Ingredient.PER: None,
                Ingredient.QUALIFIERS: [{
                    Ingredient.QTY: 4,
                    Ingredient.UNIT: 'ea',
                    Ingredient.PER: None,

                }],
            }, {
                Ingredient.QTY: 232,
                Ingredient.UNIT: 'g',
                Ingredient.PER: None,
                Ingredient.QUALIFIERS: [{
                    Ingredient.QTY: 4,
                    Ingredient.UNIT: 'ea',
                    Ingredient.PER: None,
                }],
            }],
            Ingredient.PRODUCT: product
        }
        self.assertEqual(Product.mass(ingredient), 232)
        ingredient[Ingredient.QTYS][1][Ingredient.PER] = 'each'
        self.assertEqual(Product.mass(ingredient), 464)

        ingredient = {
            Ingredient.PRODUCT: product,
            'qtys': [
                {'unit': 'ea', 'qty': 1.0, 'per': None, 'qualifiers': [
                    {'unit': 'ounce', 'qty': 4.0, 'per': None, 'qualifiers': []}
                ]}
            ],
            'names': ['mussel'],
            'mods': ['smoked'],
            'stripped_words': ['can']
        }
        self.assertEqual(Product.mass(ingredient), 113.398)

    def test_food_value(self):
        product = {'ed': 1000}
        self.assertEqual(Product.food_values(product), {'ed': (1000, 100)})
        product = {'ed': 1000, 'of': 500}
        self.assertEqual(Product.food_values(product), {
                         'ed': (1000, 100), 'of': (500, 100)})

        with patch.object(
                Product, '_db',
                {
                    'test_thing': {'of': 1.0},
                    'test_thing_2': {'of': 0.5, 'fv': 0.4}
                }):
            product = {'super': {'test_thing': 100}}
            self.assertEqual(Product.food_values(product), {
                'of': (1.0, 1.0)})
            product = {'super': {'test_thing': 50}}
            self.assertEqual(Product.food_values(product), {
                'of': (0.5, 0.5)})

            product = {'super': {'test_thing': 50, 'test_thing_2': 50}}
            self.assertEqual(Product.food_values(product), {
                'of': (0.75, 1.0),
                'fv': (0.2, 0.5)
            })

    def test_lookup(self):
        self.assertEqual(Product.lookup({'names': ['potato']})[
                         0]['name'], 'potatoes')
        self.assertEqual(Product.lookup({'names': ['potats']})[
                         0], None)
        self.assertEqual(Product.lookup({'names': ['sweet potato']})[
                         0]['name'], 'potatoes')
        self.assertEqual(Product.lookup({'names': ['sweet potato']})[
                         0]['alias'], 'sweet potato')

    def test_ghg_efficiency_ratio(self):
        with patch.object(Product, 'efficiency_baseline', return_value={'of': 2.0, 'fv': 3.0}):
            with patch.object(Product, 'ghg_value', return_value=7.5):
                product = {'of': 1.0}
                self.assertEqual(Product.ghg_efficiencies(product, None), {
                    'of': (1.0/7.5, 100)})

                self.assertEqual(
                    Product.ghg_efficiency_ratio(product), 1.0/7.5/2.0)

                with patch.object(
                        Product, '_db',
                        {
                            'test_thing': {'of': 1.0},
                            'test_thing_2': {'of': 0.5, 'fv': 0.4}
                        }):
                    product = {'super': {'test_thing': 50}}
                    self.assertEqual(Product.ghg_efficiencies(product, None), {
                        'of': (0.5/7.5, 0.5)})

                    self.assertEqual(
                        Product.ghg_efficiency_ratio(product), 0.5/7.5/2.0)

                    product = {'super': {'test_thing': 50, 'test_thing_2': 50}}
                    self.assertEqual(Product.ghg_efficiencies(product, None),
                                     {
                        'of': (0.75/7.5, 1.0),
                        'fv': (0.2/7.5, 0.5)
                    })

                    self.assertEqual(
                        Product.ghg_efficiency_ratio(product),
                        ((0.75/7.5*1.0/2.0) + (0.2/7.5*0.5/3.0)) / 1.5
                    )

                    product = {'of': 1.0, 'super': {
                        'test_thing': 50, 'test_thing_2': 50}}
                    self.assertEqual(
                        Product.ghg_efficiency_ratio(product), 1.0/7.5/2.0)

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
