#!/usr/bin/env python
from collections import defaultdict
from enum import Enum
from ghgi.parser import pad_punctuation
import json
import copy
from .datasets import MASTER_PRODUCTS
from .trigram import Trigram
from .gin import Gin
from .convert import Convert
from .origin import Origin, GHGFlavor


class Category(Enum):
    ENERGY_DENSITY = 'ed'
    PROTEIN_DENSITY = 'pd'
    OIL_FAT = 'of'
    MILK = 'm'
    ROOT = 'r'
    FRUIT_VEG = 'fv'
    SUGAR = 's'
    CAFFEINE = 'caf'
    COCOA = 'coc'


class Ingredient:
    QTYS = 'qtys'
    QTY = 'qty'
    QUALIFIERS = 'qualifiers'
    UNIT = 'unit'
    PRODUCT = 'product'
    EA = 'ea'
    PER = 'per'
    BUNCH = 'bunch'
    PKG = 'pkg'


class Product:
    _db = {}
    _baselines = {}
    NAME = 'name'
    NAMES = 'names'
    ALIAS = 'alias'
    PARENTS = 'super'
    MASS = 'g'
    SG = 'sg'
    LOSS = 'loss'  # loss in creation, e.g. whole fruit -> juice
    BUNCH = 'bunch'
    PKG = 'pkg'

    @classmethod
    def db(cls):
        if not cls._db:
            with open(MASTER_PRODUCTS) as p:
                cls._db = json.load(p)
            hidden = [k for k in cls._db if k.startswith('_')]
            for k in hidden:
                del cls._db[k]
            for k in cls._db:
                cls._db[k][Product.NAME] = k
        return cls._db

    @classmethod
    def efficiency_baselines(cls):
        """ Return a dictionary of the baseline ghg_enery_efficiency for each
        food category
        """
        if not cls._baselines:
            baselines = {o: {} for o in Origin.ORIGINS}
            for product in cls.db():
                for origin in Origin.ORIGINS:
                    ghg_values = Product.ghg_efficiencies(
                        cls.db()[product], origin)
                    for cat, values in ghg_values.items():
                        if not values[1]:
                            continue
                        if cat in baselines[origin]:
                            baselines[origin][cat] += [values[0]]
                        else:
                            baselines[origin][cat] = [values[0]]

            for origin in baselines:
                for k in baselines[origin]:
                    baselines[origin][k].sort(reverse=True)
                    if len(baselines[origin][k]) <= 1:
                        # no meaningful comparison possible
                        baselines[origin][k] = None
                    elif len(baselines[origin][k]) <= 6:
                        baselines[origin][k] = baselines[origin][k][0]
                    else:
                        baselines[origin][k] = baselines[origin][k][1]
            cls._baselines = baselines
        return cls._baselines

    @classmethod
    def expanded_baselines(cls):
        baselines = {o: {} for o in Origin.ORIGINS}
        for product in cls.db():
            for origin in Origin.ORIGINS:
                ghg_values = Product.ghg_efficiencies(
                    cls.db()[product], origin)
                for cat, values in ghg_values.items():
                    if not values[1]:
                        continue
                    if cat in baselines[origin]:
                        baselines[origin][cat] += [values[0]]
                    else:
                        baselines[origin][cat] = [values[0]]
                for k in baselines[origin]:
                    baselines[origin][k].sort(reverse=True)
        return baselines

    @classmethod
    def efficiency_baseline(cls, origin):
        return cls.efficiency_baselines()[origin]

    @staticmethod
    def get(db_name, alias=None):
        # return a copy of the product entry, with its .ALIAS value set to
        # a provided alias or None
        result = copy.deepcopy(Product.db().get(db_name))
        if result is not None:
            result.update({Product.NAME: db_name, Product.ALIAS: alias})
        return result

    @staticmethod
    def lookup(ingredient):
        # given a list of names for a product, return the match with the
        # highest confidence
        if not Product.NAMES in ingredient:
            return (None, None)
        results = []
        for name in ingredient[Product.NAMES]:
            # [(parent id, aka, confidence),...]
            name = name.replace('-', ' ')
            # matches = Trigram.match(name)
            match = Gin.query(name)
            if match[0] is not None:
                product = Product.get(match[1][0], match[0])
                confidence = match[2]
                results += [(product, confidence)]
        # results.sort(key=lambda k: k[1], reverse=True)
        return results[0] if results else (None, None)

    @staticmethod
    def itemize(ingredients):
        """match user ingredient terms to our database in-place"""
        for ingredient in ingredients:
            (ingredient[Ingredient.PRODUCT],
             ingredient['match_conf']) = Product.lookup(ingredient)

    @staticmethod
    def sg(product):
        # parent values are dicts of {parent: percentage} where the
        # percentage is the percent amount of the parent per 100 of the
        # product. So a 50/50 mix would have parents {x: 50, y: 50},
        # and a concentrate might have parents {x: 400}. Products can override
        # their parents' `sg` and `g` values to inherit only their ghg values.
        sg = product.get(Product.SG)
        if (not sg) and product.get(Product.PARENTS):
            sg = 0
            for parent, percentage in product[Product.PARENTS].items():
                par_sg = Product.sg(Product.get(parent))
                if par_sg:
                    sg += par_sg * percentage/100.0

        return sg

    @staticmethod
    def g(product):
        if product.get(Product.MASS):
            return product[Product.MASS]
        parents = product.get(Product.PARENTS)
        if not parents:
            return 0.0
        return sum([Product.g(Product.get(parent)) * percentage/100.0 for parent, percentage in parents.items()])

    @staticmethod
    def unbundle(product, qty, unit):
        """ Convert pkg and bunch units to qty, other_unit """
        if unit == Ingredient.BUNCH:
            if product.get(Product.BUNCH):
                return qty * product.get(Product.BUNCH), Ingredient.EA
            parents = product.get(Product.PARENTS)
            if len(parents) == 1:
                parent = Product.get(list(parents.keys())[0])
                return Product.unbundle(parent, qty, unit)
            else:  # default
                return qty * 6, Ingredient.EA

        elif unit == Ingredient.PKG:
            if product.get(Product.PKG):
                return qty * product.get(Product.PKG), 'ml'
            parents = product.get(Product.PARENTS)
            if len(parents) == 1:
                parent = Product.get(list(parents.keys())[0])
                return Product.unbundle(parent, qty, unit)
            else:  # default
                return qty * 540, 'ml'

        return qty, unit

    @staticmethod
    def mass(ingredient):
        """Return the mass in grams of the ingredient product.
        The ingredient should include a value under 'product' which is its
        looked-up product entry.

        TODO: This gets a bit tricky for things like cans, bunches, and sprigs, which
        are essentially different sizes of `ea`. In addition to the default 
        "g" value, I think we need to add something optional like `single_g`,
        `agg_g` and introduce new units `single`, `agg` which would be used
        to mask thinks like `sprig`, `bunch`, and so forth.

        Ingredients can have multiple quantity values. `ea` values are notably
        tricky. If we get one, we first check if there is a non-ea unit
        qualifier, in which case we can multiply its value by the `ea` count
        and generate a combined value in the qualifier's units. For instance,
        if we have 2 `ea` of something qualified as 3 `pounds`, the `qty` becomes
        2*3 = 6, and the unit goes from `ea` to `pounds`.
        """

        product = ingredient[Ingredient.PRODUCT]
        sg = Product.sg(product)
        qtys = ingredient[Ingredient.QTYS][0]
        qty = qtys[Ingredient.QTY]
        unit = qtys[Ingredient.UNIT]

        if unit not in [Ingredient.EA, Ingredient.PKG, Ingredient.BUNCH]:
            return Convert.to_metric(qty, unit, sg)

        # see if there is clarification available for the value
        for qual in qtys.get(Ingredient.QUALIFIERS, []):
            if qual[Ingredient.UNIT] != Ingredient.EA:
                unit = qual[Ingredient.UNIT]
                if qual.get(Ingredient.PER) == 'each':
                    qty = qty * qual[Ingredient.QTY]
                else:
                    qty = qual[Ingredient.QTY]
                return Convert.to_metric(qty, unit, sg)

        # if there was no clarification in the qualifiers, see if a
        # subsequent quantity offers any help
        for sub in ingredient[Ingredient.QTYS][1:]:
            if sub[Ingredient.UNIT] != Ingredient.EA:
                unit = sub[Ingredient.UNIT]
                if sub.get(Ingredient.PER) == 'each':
                    qty = qty * sub[Ingredient.QTY]
                else:
                    qty = sub[Ingredient.QTY]
                return Convert.to_metric(qty, unit, sg)

        # if there were no clarifications, unbundle
        qty, unit = Product.unbundle(product, qty, unit)

        if unit == Ingredient.EA:
            qty *= Product.g(product)

        return Convert.to_metric(qty, unit, sg)

    @staticmethod
    def ghg_value(product, origin, flavor: GHGFlavor):
        if product is None:
            return 0.0
        value = Origin.ghg_value(product[Product.NAME], origin, flavor)
        if (value is None) and product[Product.PARENTS]:
            value = 0.0
            for parent, pct in product[Product.PARENTS].items():
                par_value = Product.ghg_value(Product.get(parent),
                                              origin, flavor)
                if par_value is not None:
                    value += par_value * pct/100.0
        return value

    @staticmethod
    def food_values(product):
        """ return a dict of {category: (value, direct)} where category is the
        product category, value is the food value of this product for that
        type, and direct is whether that value was generated directly or as a
        composite of parents.
        """
        if not product:  # empty or None
            return {}
        values = defaultdict(lambda: (0.0, False))
        for cat in Category:
            value = product.get(cat.value, None)
            if value:
                values[cat.value] = (value, True)
        if values:
            return values

        # derive values from parents if not available directly
        for parent, pct in product.get(Product.PARENTS, {}).items():
            # This assumes that the net food values do not change. So 100g of juice
            # has the same food value as 100g of whole fruit, but its CO2 impact is
            # a multiple based on the LOSS value. Clearly, this isn't true in all
            # or even most cases, and as such food values should be overwritten
            # where known.
            par_values = Product.food_values(Product.get(parent))
            for cat in par_values:
                value = values[cat][0] + \
                    (par_values[cat][0] * pct/100.0)
                values[cat] = value,  False  # indirect
        return values

    @staticmethod
    def ghg_efficiency_ratio(product, origin=Origin.DEFAULT):
        # For a single-category item, return the ratio between this one's
        # efficiency in that category and the baseline.
        if product is None:
            return None
        prod_efficiencies = Product.ghg_efficiencies(product, origin)
        for cat in Category:
            if not prod_efficiencies.get(cat.value, [None, False])[1]:
                continue
            baseline = Product.efficiency_baseline(origin)[cat.value]
            if baseline:
                return prod_efficiencies[cat.value][0]/baseline
        # If it has parents, return the weighted average of their efficiency ratios.
        value = None
        total_pct = 0
        for parent, pct in product.get(Product.PARENTS, {}).items():
            ghg_eff = Product.ghg_efficiency_ratio(
                Product.get(parent), origin)
            if ghg_eff:
                value = value if value else 0.0  # convert from None if needed
                loss = product.get(Product.LOSS, {}).get(parent, 0.0)
                value += ghg_eff * (1.0-loss) * pct
                total_pct += pct
        if value and (total_pct > 0):
            value /= total_pct
        return value

    @staticmethod
    def ghg_efficiencies(product, origin):
        """ return ghg_mean emission per Category """
        ghg_mass_mean = Product.ghg_value(product, origin, GHGFlavor.MEAN)
        if not ghg_mass_mean:
            return {}
        return {cat: (value[0]/ghg_mass_mean, value[1]) for cat, value in Product.food_values(product).items()}

    @staticmethod
    def impact(ingredient, origin=Origin.DEFAULT):
        if ingredient.get('error') or (ingredient.get(Ingredient.PRODUCT) is None):
            return 0.0
        mass = Product.mass(ingredient)
        ingredient[Product.MASS] = mass
        ghg_mean = Product.ghg_value(
            ingredient[Ingredient.PRODUCT],
            origin, GHGFlavor.MEAN
        )
        result = round(ghg_mean * mass, 2) if ghg_mean else None
        ingredient['impact'] = result
        return result
