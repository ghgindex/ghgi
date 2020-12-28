#!/usr/bin/env python
import os
import json
import pathlib


def sortify(element):
    """in-place sort of list elements"""
    if not element:
        return
    if type(element) is dict:
        for k in element:
            sortify(element[k])
    elif type(element) is list:
        if all([type(el) is str for el in element]):
            element.sort()


def akaify(products):
    """ Extend aka list based on product variants """
    for k in products:
        if not 'vars' in products[k]:
            continue
        for var_type in products[k]['vars']:
            for base in products[k]['vars'][var_type]:
                for var in products[k]['vars'][var_type][base]:
                    paired = ' '.join([var, base])
                    try:
                        if not paired in products[k].get('aka', []):
                            products[k]['aka'] += [paired]
                        if var_type == 'standalone':
                            if not var in products[k].get('aka', []):
                                products[k]['aka'] += [var]
                    except Exception as e:
                        print(products[k])
                        raise e
        products[k]['aka'] = list(set(products[k].get('aka', [])))


def clean():
    """iterate the values of the json dicts and sort any lists"""
    path = pathlib.Path(__file__).parent.absolute()
    for file in ['products.json', 'origins.json', 'sources.json']:
        with open(os.path.join(path, file), 'r') as f:
            inputs = json.load(f)
        if file == 'products.json':
            akaify(inputs)
        sortify(inputs)
        with open(os.path.join(path, file), 'w') as f:
            json.dump(inputs, f, indent=4, sort_keys=True)


def unique_names():
    path = pathlib.Path(__file__).parent.absolute()
    seen = set()
    with open(os.path.join(path, 'products.json'), 'r') as f:
        inputs = json.load(f)
        for k, v in inputs.items():
            if type(v) == str:
                continue
            if k in seen:
                print('name {} already seen!'.format(k))
            seen.add(k)
            for aka in v.get('aka', []):
                if aka in seen and not aka == k:
                    print('aka {} already seen!'.format(aka))
                seen.add(aka)


def validate():
    # validate origins via checksum
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


if __name__ == "__main__":
    clean()
    unique_names()
    # validate()
