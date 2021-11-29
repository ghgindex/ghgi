from unittest import TestCase
from unittest.mock import patch

from ghgi.product import Product, Category, Ingredient


class TestProduct(TestCase):
    def test_products_valid(self):
        # validate that all products have requisite minimal data:
        # mass, specific gravity, and category OR a super.
        for product in Product.db().values():
            if not Product.valid(product):
                self.fail('Product {} has invalid data.'.format(
                    product[Product.NAME]))

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
                Ingredient.PLUS: False
            }],
        }
        # test dummy
        self.assertEqual(Product.mass(ingredient), 200)
        ingredient[Ingredient.PRODUCT] = {}
        self.assertEqual(Product.mass(ingredient), 200)

        ingredient[Ingredient.PRODUCT] = product
        self.assertEqual(Product.mass(ingredient), 200)

        ingredient[Ingredient.QTYS] = [{
            Ingredient.QTY: 200, Ingredient.UNIT: 'ml', Ingredient.PER: None, Ingredient.PLUS: False}]
        self.assertEqual(Product.mass(ingredient), 400)

        ingredient[Ingredient.QTYS] = [{
            Ingredient.QTY: 110, Ingredient.UNIT: 'g', Ingredient.PER: None, Ingredient.PLUS: False}]
        self.assertEqual(Product.mass(ingredient), 110)

        ingredient[Ingredient.QTYS] = [{
            Ingredient.QTY: 2, Ingredient.UNIT: 'pkg', Ingredient.PER: None, Ingredient.PLUS: False}]
        self.assertEqual(Product.mass(ingredient), 2160)

        product['pkg'] = 125
        self.assertEqual(Product.mass(ingredient), 500)

        ingredient[Ingredient.QTYS] = [{
            Ingredient.QTY: 2, Ingredient.UNIT: 'bunch', Ingredient.PER: None, Ingredient.PLUS: False}]
        self.assertEqual(Product.mass(ingredient), 1200)

        product['bunch'] = 10
        self.assertEqual(Product.mass(ingredient), 2000)

        del product['pkg']
        del product['bunch']
        product[Product.PARENTS] = {'parent': 100}
        with patch.object(Product, '_db', {'parent': {'pkg': 800, 'bunch': 8}, }):
            ingredient[Ingredient.QTYS] = [{
                Ingredient.QTY: 2, Ingredient.UNIT: 'bunch', Ingredient.PER: None, Ingredient.PLUS: False}]
            self.assertEqual(Product.mass(ingredient), 1600)

            ingredient[Ingredient.QTYS] = [{
                Ingredient.QTY: 2, Ingredient.UNIT: 'pkg', Ingredient.PER: None, Ingredient.PLUS: False}]
            self.assertEqual(Product.mass(ingredient), 3200)

        ingredient[Ingredient.QTYS] = [
            {
                Ingredient.QTY: 20, Ingredient.UNIT: 'ml',
                Ingredient.PER: None, Ingredient.PLUS: False
            },
            {
                Ingredient.QTY: 1500, Ingredient.UNIT: 'g',
                Ingredient.PER: None, Ingredient.PLUS: False
            },
        ]
        self.assertEqual(Product.mass(ingredient), 1500)

    def test_food_value(self):
        # TODO: fix these tests; they're kind of crap
        with patch.object(Product, 'fv_db', return_value={
            'test_product': {'ed': 1000},
            'test_product_2': {'ed': 1000, 'of': 500},
            'test_super_1': {'of': 1.0},
            'test_super_2': {'of': 0.5, 'fv': 0.4}
        }):
            product = {'name': 'test_product'}
            self.assertEqual(Product.food_values(product), {'ed': 1000})
            product = {'ed': 1000, 'of': 500}
            product = {'name': 'test_product_2'}
            self.assertEqual(Product.food_values(product), {
                'ed': 1000, 'of': 500})

            with patch.object(
                    Product, '_db', {
                        'test_super_1': {'name': 'test_super_1'},
                        'test_super_2': {'name': 'test_super_2'},
                    }):
                product = {'name': 'test_product_3',
                           'super': {'test_super_1': 100}}
                self.assertEqual(Product.food_values(product), {})
                product = {'name': 'test_product_3',
                           'super': {'test_super_1': 50}}
                self.assertEqual(Product.food_values(product), {})

                product = {'name': 'test_product_3', 'super': {
                    'test_super_1': 50, 'test_super_2': 50}}
                self.assertEqual(Product.food_values(product), {})

    def test_lookup(self):
        # self.assertEqual(Product.lookup({'names': ['tuna', 'chickpea', 'white bean']})[
        #                  0]['alias'], 'tuna')
        self.assertEqual(Product.lookup({'names': ['grape', 'cherry tomato']})[
                         0]['alias'], 'cherry tomato')
        self.assertEqual(Product.lookup({'names': ['potato']})[
                         0]['name'], 'potatoes')
        self.assertEqual(Product.lookup({'names': ['potats']})[
                         0], None)
        self.assertEqual(Product.lookup({'names': ['sweet potato']})[
                         0]['name'], 'potatoes')
        self.assertEqual(Product.lookup({'names': ['sweet potato']})[
                         0]['alias'], 'sweet potato')

    def test_ghg_efficiency_parents(self):
        result = Product.lookup({'names': ['chicken stock']})
        eff = Product.ghg_efficiency_ratio(result[0])

    def test_ghg_efficiency_ratio(self):
        with patch.object(Product, 'efficiency_baseline', return_value={'of': 2.0, 'fv': 3.0}):
            with patch.object(Product, 'fv_db', return_value={
                'test_product': {'of': 1.0},
                'test_super': {'of': 1.0},
                'test_super_2': {'fv': 0.3}
            }):
                with patch.object(Product, 'ghg_value', return_value=7.5):
                    product = {'name': 'test_product'}
                    self.assertEqual(Product.ghg_efficiencies(product, None), {
                        'of': 1.0/7.5})

                    self.assertEqual(
                        Product.ghg_efficiency_ratio(product), 1.0/7.5/2.0)

                    with patch.object(
                            Product, '_db',
                            {
                                'test_super': {'name': 'test_super'},
                                'test_super_2': {'name': 'test_super_2'}
                            }):
                        product = {'name': 'test_product_2',
                                   'super': {'test_super': 50}}
                        self.assertEqual(
                            Product.ghg_efficiencies(product, None), {})

                        self.assertEqual(
                            Product.ghg_efficiency_ratio(product), 1.0/7.5/2.0)
                        product = {'name': 'test_product_2',
                                   'super': {'test_super': 100}}
                        self.assertEqual(
                            Product.ghg_efficiency_ratio(product), 1.0/7.5/2.0)

                        product = {'name': 'test_product_2', 'super': {
                            'test_super': 50,
                            'test_super_2': 50
                        }}

                        result = 1 / (((50 / (0.3 / 7.5 / 3.0)) +
                                      (50 / (1.0 / 7.5 / 2.0))) / 100)
                        self.assertEqual(
                            Product.ghg_efficiency_ratio(product), result)

                        product = {'name': 'test_product', 'super': {
                            'test_super': 50,
                            'test_super_2': 50
                        }}
                        self.assertEqual(
                            Product.ghg_efficiency_ratio(product), 1.0/7.5/2.0)

    def test_labels(self):
        pass
