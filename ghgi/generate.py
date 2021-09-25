#!/usr/bin/env python
from ghgi.product import Product
import json


from .trigram import build_indexes
from .gin import GIN
from .datasets import SOURCE_PRODUCTS
from .datasets import MASTER_GIN_INDEX
from .origin import Origin
from .datasets import MASTER_PRODUCTS, MASTER_AKA_INDEX, MASTER_TRIGRAM_INDEX


def sort_data(data, sort_lists=False):
    if type(data) is dict:
        data = {k: sort_data(data[k], sort_lists=sort_lists)
                for k in sorted(data)}
    elif type(data) is list:
        if sort_lists and all([type(d) is str for d in data]):
            try:
                data = sorted(data)
            except Exception as err:
                print('unable to sort {}'.format(data))
                print(err)

    return data


def sort_products(infile_path, outfile_path=None):
    """ Given an infile json dictionary, sort it by its keys,
    sort sub-dictionaries by their keys, and sort the contents of lists of
    strings.
    """
    if outfile_path is None:
        # if no outfile_path is provided, write back to infile_path
        outfile_path = infile_path

    with open(infile_path, 'r') as infile:
        products = json.load(infile)
        products = sort_data(products, sort_lists=True)

    with open(outfile_path, 'w') as outfile:
        json.dump(products, outfile, indent=4)


def sort_origin(infile_path, outfile_path=None):
    if outfile_path is None:
        # if no outfile_path is provided, write back to infile_path
        outfile_path = infile_path

    with open(infile_path, 'r') as infile:
        origin = json.load(infile)
        origin = sort_data(origin, sort_lists=False)

    with open(outfile_path, 'w') as outfile:
        json.dump(origin, outfile, indent=4)


def extend_products(infile, outfile):
    products = json.load(infile)
    extended_products = {}
    for product, values in products.items():
        if product.startswith('_'):
            continue
        extended_names = [product]
        for name, extensions in values.get('names', {}).items():
            if name.startswith('~'):
                name = name[1:]
            else:
                extended_names += [name]
            for k, extension_names in extensions.items():
                for extension in extension_names:
                    trailing = '_' in extension[:2]
                    no_space = '.' in extension[:2]
                    if trailing:
                        extension = extension[1:]
                    if no_space:
                        extension = extension[1:]
                    pair = (name, extension) if trailing else (extension, name)
                    separator = '' if no_space else ' '
                    extended_names += [separator.join(pair)]
                    if k == 'independent':
                        extended_names += [extension]
        extended_names = list(set(extended_names))
        extended_names.sort()
        values['names'] = extended_names
        extended_products[product] = values
    master_names = set()
    for product in extended_products.values():
        for name in product['names']:
            if name in master_names:
                raise Exception('{} already used!'.format(name))
        master_names |= set(product['names'])
    json.dump(extended_products, outfile, indent=4)
    return extended_products


if __name__ == "__main__":
    sort_products(SOURCE_PRODUCTS)
    for origin in Origin.ORIGIN_PATHS.values():
        sort_origin(origin)

    # create the un-localized master products database
    with open(SOURCE_PRODUCTS) as f:
        with open(MASTER_PRODUCTS, 'w') as outfile:
            extended = extend_products(f, outfile)

    # validate products
    Product.validate_db()

    with open(MASTER_PRODUCTS, 'r') as products:
        aka_index, trigram_index = build_indexes(products)
        print('There are {} aliases in the database.'.format(len(aka_index)))
        with open(MASTER_AKA_INDEX, 'w') as aka_file:
            json.dump(aka_index,  aka_file, indent=4)
        with open(MASTER_TRIGRAM_INDEX, 'w') as tri_file:
            json.dump(trigram_index, tri_file, indent=4)

    gin_index = GIN.generate()
    with open(MASTER_GIN_INDEX, 'w') as gin_file:
        json.dump(gin_index, gin_file, indent=4)

    # TODO: there should be some sort of check on the origins. Maybe via test?
