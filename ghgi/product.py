#!/usr/bin/env python
import os
import pathlib
from collections import defaultdict
from enum import Enum
import json
import copy
from .datasets import MASTER_PRODUCTS
from .trigram import Trigram
from .convert import Convert
from .origin import Origin

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
        result = copy.deepcopy(Product.db().get(db_name))
        if result is not None:
            result.update({Product.NAME: db_name, Product.ALIAS: alias})
        return result

    @staticmethod
    def lookup(ingredient, version=1):
        if version == 1:
            if not Product.NAME in ingredient:
                return (None, None)
            name, confidence = ingredient[Product.NAME]
            matches = Trigram.match(name)  # [(parent id, aka, confidence),...]
            if matches:
                product = Product.get(matches[0][0], matches[0][1])
                confidence *= matches[0][2]
                return product, confidence
            return (None, None)
        elif version == 2:
            if not Product.NAMES in ingredient:
                return (None, None)
            results = []
            for name in ingredient[Product.NAMES]:
                # [(parent id, aka, confidence),...]
                name = name.replace('-', ' ')
                matches = Trigram.match(name)
                if matches:
                    product = Product.get(matches[0][0], matches[0][1])
                    confidence = matches[0][2]
                    results += [(product, confidence)]
            results.sort(key=lambda k: k[1], reverse=True)
            return results[0] if results else (None, None)

    @staticmethod
    def itemize(ingredients, version=2):
        """match user ingredient terms to our database in-place"""
        for ingred in ingredients:
            (ingred['product'], ingred['match_conf']) = Product.lookup(
                ingred, version=version)

    @staticmethod
    def sg(product):
        # parent values are dicts of {parent: percentage} where the
        # percentage is the percent amount of the parent per 100 of the
        # product. So a 50/50 mix would have parents {x: 50, y: 50},
        # and a concentrate might have parents {x: 400}. Products can override
        # their parents' `sg` and `g` values to inherit only their ghg values.
        sg = product.get(Product.SG)
        if (not sg) and product.get(Product.PARENTS):
            return sum([Product.sg(Product.get(parent)) * percentage/100.0 for parent, percentage in product['par'].items()])
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
    def mass(ingredient, version=2):
        """Return the mass in grams of the ingredient"""
        if version == 1:
            qty = ingredient['qty'][0]
            unit = ingredient.get('unit')[0]
        elif version == 2:
            qty = ingredient['qtys'][0]['qty'][0]
            unit = ingredient['qtys'][0].get('unit')[0]
        sg = Product.sg(ingredient['product'])
        if unit == 'ea':
            qty *= Product.g(ingredient['product'])
        return Convert.convert(qty, unit, sg)

    @staticmethod
    def ghg_value(flavor, product, origin):
        if product is None:
            return 0.0
        value = Origin.ghg_value(flavor, product[Product.NAME], origin)
        if (value is None) and product[Product.PARENTS]:
            value = 0.0
            for parent, pct in product[Product.PARENTS].items():
                par_value = Product.ghg_value(flavor, Product.get(parent),
                                              origin)
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
        values = defaultdict(lambda: (0.0, False))
        if product is None:
            return values
        for cat in Category:
            value = product.get(cat.value, None)
            if value:
                values[cat.value] = (value, True)
        if values:
            return values
        # derive values from parents if not available directly
        for parent, pct in product.get(Product.PARENTS, {}).items():
            par_values = Product.food_values(Product.get(parent))
            for cat in par_values:
                value = values[cat][0] + \
                    (par_values[cat][0] * pct/100.0)
                values[cat] = value,  False  # indirect
        return values

    @staticmethod
    def ghg_efficiency_ratio(product, origin):
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
        ghg_mass_mean = Product.ghg_value(Origin.GHG_MEAN, product, origin)
        if not ghg_mass_mean:
            return {}
        return {cat: (value[0]/ghg_mass_mean, value[1]) for cat, value in Product.food_values(product).items()}

    @staticmethod
    def impact(ingredient, origin=Origin.GLOBAL, version=2):
        if ingredient.get('error') or (ingredient.get('product') is None):
            return 0.0
        mass = Product.mass(ingredient, version)
        ingredient[Product.MASS] = mass
        ghg_mean = Product.ghg_value(
            Origin.GHG_MEAN, ingredient['product'], origin)
        result = round(ghg_mean * mass, 2) if ghg_mean else None
        ingredient['impact'] = result
        return result
