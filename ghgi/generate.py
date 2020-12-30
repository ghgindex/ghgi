#!/usr/bin/env python
import os
import json


from trigram import build_indexes
from datasets import SOURCE_PRODUCTS
from datasets import MASTER_PRODUCTS, MASTER_AKA_INDEX, MASTER_TRIGRAM_INDEX

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
                    trailing =  '_' in extension[:2]
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
    json.dump(extended_products, outfile)
    return extended_products


if __name__ == "__main__":
    # create the un-localized master products database
    with open(SOURCE_PRODUCTS) as f:
        with open(MASTER_PRODUCTS, 'w') as outfile:
            extended = extend_products(f, outfile)

    with open(MASTER_PRODUCTS, 'r') as products:
        aka_index, trigram_index = build_indexes(products)
        with open(MASTER_AKA_INDEX, 'w') as aka_file:
            json.dump(aka_index,  aka_file)
        with open(MASTER_TRIGRAM_INDEX, 'w') as tri_file:
            json.dump(trigram_index, tri_file)
    
    # TODO: there should be some sort of check on the origins. Maybe via test?
