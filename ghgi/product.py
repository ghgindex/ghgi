#!/usr/bin/env python
from collections import defaultdict
from enum import Enum
from ghgi.parser import pad_punctuation
import json
import copy
from .datasets import MASTER_PRODUCTS
from .trigram import Trigram
from .gin import GIN
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
    PLUS = 'plus'
    MODS = 'mods'


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
    def validate_db(cls):
        """ Validate that all products in database have, directly or via their
        `super`, the keys [Product.NAME, Product.MASS, and Product.SG] and a value
        for at least one Category.
        """
        valid = True
        for name, product in cls.db().items():
            if not name:
                valid = False
                print('product name must not be blank')
            elif name.startswith('_'):
                # ignore these
                continue

            if Product.sg(product) is None:
                valid = False
                print('no sg value found for {}'.format(name))

            if Product.g(product) in [None, 0.0]:
                valid = False
                print('no g (mass) value found for {}'.format(name))

        if not valid:
            raise Exception('Product database failed to validate')

    @classmethod
    def efficiency_baselines(cls):
        """ Return a dictionary of the baseline ghg_energy_efficiency for each
        food category
        """
        if not cls._baselines:
            baselines = {o: {} for o in Origin.ORIGINS}
            for product in cls.db():
                for origin in Origin.ORIGINS:
                    ghg_values = Product.ghg_efficiencies(
                        cls.db()[product], origin)
                    for cat, value in ghg_values.items():
                        if not value:
                            continue
                        if cat in baselines[origin]:
                            baselines[origin][cat] += [value]
                        else:
                            baselines[origin][cat] = [value]

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
                for cat, value in ghg_values.items():
                    if not value:
                        continue
                    if cat in baselines[origin]:
                        baselines[origin][cat] += [value]
                    else:
                        baselines[origin][cat] = [value]
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
            name = name.replace('-', ' ')
            size = len(name)
            match = GIN.query(name)
            if match[0] is not None:
                product = Product.get(match[1][0], match[0])
                confidence = match[2]
                results += [(product, confidence, size)]
        results.sort(key=lambda k: k[2], reverse=True)  # prefer longer matches
        results.sort(key=lambda k: k[1], reverse=True)
        return results[0][:2] if results else (None, None)

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
    def mass_for_entry(sg, entry):
        """
        Return the inferred mass, the quantity type, and whether it's a plus.

        TODO: This gets a bit tricky for things like cans, bunches, and sprigs, which
        are essentially different sizes of `ea`. In addition to the default 
        "g" value, I think we need to add something optional like `single_g`,
        `agg_g` and introduce new units `single`, `agg` which would be used
        to mask thinks like `sprig`, `bunch`, and so forth.

        We prefer mass units to volumes or `ea`ches.

        Ingredients can have multiple quantity values. `ea` values are notably
        tricky. If we get one, we first check if there is a non-ea unit
        qualifier, in which case we can multiply its value by the `ea` count
        and generate a combined value in the qualifier's units. For instance,
        if we have 2 `ea` of something qualified as 3 `pounds`, the `qty` becomes
        2*3 = 6, and the unit goes from `ea` to `pounds`.
        """
        flavor = None

        qty = entry[Ingredient.QTY]
        plus = entry[Ingredient.PLUS]
        unit = entry[Ingredient.UNIT]
        per = entry[Ingredient.PER]

        if unit in Convert.VOLUME:
            flavor = Convert.VOLUME
        elif unit in Convert.MASS:
            flavor = Convert.MASS

        if unit not in [Ingredient.EA, Ingredient.PKG, Ingredient.BUNCH]:
            return Convert.to_metric(qty, unit, sg), flavor, plus, per

        # see if there is clarification available for the value
        for qual in entry.get(Ingredient.QUALIFIERS, []):
            if qual[Ingredient.UNIT] != Ingredient.EA:
                unit = qual[Ingredient.UNIT]
                if unit in Convert.VOLUME:
                    flavor = Convert.VOLUME
                elif unit in Convert.MASS:
                    flavor = Convert.MASS
                if qual.get(Ingredient.PER) == 'each':
                    qty = qty * qual[Ingredient.QTY]
                else:
                    qty = qual[Ingredient.QTY]
                return Convert.to_metric(qty, unit, sg), flavor, plus, per

        return qty, unit, plus, per

    @staticmethod
    def mass(ingredient):
        """Return the mass in grams of the ingredient product.
        The ingredient should include a value under 'product' which is its
        looked-up product entry.

        This function assesses all of the available quantity information and
        tries to synthesize it in the most accurate way possible.
        """

        product = ingredient[Ingredient.PRODUCT]
        sg = Product.sg(product)
        mods = ingredient.get(Ingredient.MODS)
        grated = mods and 'grated' in mods

        converted_qtys = [
            Product.mass_for_entry(sg, q) for q in ingredient[Ingredient.QTYS]
        ]

        if converted_qtys[0][1] in [Ingredient.EA, Ingredient.PKG, Ingredient.BUNCH]:
            # see if we can find a clarification
            qty = converted_qtys[0][0]
            unit = converted_qtys[0][1]
            for sub in converted_qtys[1:]:
                if sub[1] != Ingredient.EA:
                    unit = sub[1]
                    if sub[3] == 'each':
                        qty = qty * sub[0]
                    else:
                        qty = sub[0]
                    return qty

            # if nothing was found, multiple the EA value by Product.g
            qty, unit = Product.unbundle(product, qty, unit)
            if unit == Ingredient.EA:
                qty *= Product.g(product)
            return Convert.to_metric(qty, unit, sg)

        # otherwise, we aggregate mass and volume entries
        mass_qty = 0
        vol_qty = 0
        plus = False
        for converted_qty in converted_qtys:
            plus |= converted_qty[2]
            if converted_qty[1] == Convert.MASS:
                if plus or (mass_qty == 0):
                    mass_qty += converted_qty[0]
            elif converted_qty[1] == Convert.VOLUME:
                if plus or (vol_qty == 0):
                    vol_qty += converted_qty[0]

        if vol_qty and grated:
            # UGLY: accounting for cheeses
            vol_qty /= 6

        if not mass_qty:
            return vol_qty
        return mass_qty

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
        """ return a dict of {category: value} where category is the
        product category, and value is the food value of this product for that
        type.
        """
        if not product:  # empty or None
            return {}
        values = defaultdict(lambda: 0.0)
        for cat in Category:
            value = product.get(cat.value, None)
            if value:
                values[cat.value] = value
        return values

    @staticmethod
    def ghg_efficiency_ratio(product, origin=Origin.DEFAULT):
        # return the ratio between this product's efficiency and its
        # baseline(s). If it has no food values, aggregate its parents'
        # ghg_efficiency_ratios
        if product is None:
            return None

        prod_efficiencies = Product.ghg_efficiencies(product, origin)

        # if prod_efficiencies isn't empty, it can only have one entry; return it
        for cat, eff in prod_efficiencies.items():
            baseline = Product.efficiency_baseline(origin)[cat]
            if baseline is None:
                return
            return eff / baseline

        # otherwise, use its parents
        share_weighted_efficiency_ratios = 0.0
        shares = 0.0
        for parent, share in product.get(Product.PARENTS, {}).items():
            parent_eff_ratio = Product.ghg_efficiency_ratio(
                Product.get(parent), origin)
            if parent_eff_ratio is None:
                continue
            shares += share
            share_weighted_efficiency_ratios += parent_eff_ratio * share

        if shares > 0:
            return share_weighted_efficiency_ratios / shares

        return None

    @staticmethod
    def ghg_efficiencies(product, origin):
        """ return product's ghg_mean emission per food Category """
        ghg_mass_mean = Product.ghg_value(product, origin, GHGFlavor.MEAN)
        if not ghg_mass_mean:
            return {}
        return {cat: value/ghg_mass_mean for cat, value in Product.food_values(product).items()}

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
