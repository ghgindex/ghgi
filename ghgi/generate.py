#!/usr/bin/env python
import json

from trigram import build_indexes
from datasets import SOURCE_PRODUCTS
from datasets import MASTER_PRODUCTS, MASTER_AKA_INDEX, MASTER_TRIGRAM_INDEX

from origin import Origin
def validate():
    # validate origins via checksum
    import pathlib, os
    path = pathlib.Path(__file__).parent.absolute()
    with open(os.path.join(path, 'origins.json'), 'r') as f:
        inputs = json.load(f)
        total = 0.0
        for k, v in inputs['global'].items():
            if type(v) is list:
                if len(v) < 5:
                    print('error in', k)
                if len(v) == 6:  # it has a note
                    total += sum(v[1:-1])
                else:
                    total += sum(v[1:])
        if round(total, 2) != 1654.27:
            print('checksum failure!!')


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

def sanity_check(new, original):
    new_names = set(new.keys())
    for values in new.values():
        new_names |= set(values['names'])
    matched_names = []
    for name, values in original.items():
        if name.startswith('_'):
            continue
        if name not in new_names:
            print('{} not found in new names'.format(name))
        else:
            matched_names += [name]
        for aka in values.get('aka', []):
            if aka not in new_names:
                print('aka {} not found in new names'.format(aka))
            else:
                matched_names += [aka]
    print('{} matched names found'.format(len(matched_names)))

if __name__ == "__main__":
    # path = pathlib.Path(__file__).parent.absolute()
    # create the un-localized master products database
    with open(SOURCE_PRODUCTS) as f:
        with open(MASTER_PRODUCTS, 'w') as outfile:
            extended = extend_products(f, outfile)
    # with open(os.path.join(path, 'datasets/products_original.json')) as f:
    #     original = json.load(f)
    # sanity_check(extended, original)
    with open(MASTER_PRODUCTS, 'r') as products:
        aka_index, trigram_index = build_indexes(products)
        with open(MASTER_AKA_INDEX, 'w') as aka_file:
            json.dump(aka_index,  aka_file)
        with open(MASTER_TRIGRAM_INDEX, 'w') as tri_file:
            json.dump(trigram_index, tri_file)
    
    # clean()
    # unique_names()
    # validate()
