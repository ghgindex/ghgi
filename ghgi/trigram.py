#!/usr/bin/env python
import json
import collections
from .datasets import MASTER_TRIGRAM_INDEX, MASTER_AKA_INDEX

class Trigram:
    # TODO: make these dicts of lazily loaded sub-indexes keyed by locales
    _product_index = {}
    _aka_index = {}

    @classmethod
    def drop_indexes(cls):
        cls._product_index = {}
        cls._aka_index = {}

    @classmethod
    def product_index(cls):
        if not cls._product_index:
            with open(MASTER_TRIGRAM_INDEX) as p:
                cls._product_index = json.load(p)
        return cls._product_index

    @classmethod
    def aka_index(cls):
        if not cls._aka_index:
            with open(MASTER_AKA_INDEX) as p:
                cls._aka_index = json.load(p)
        return cls._aka_index

    @classmethod
    def match(cls, term):
        """Return a list of matching products and match percent"""
        termgram = cls.trigrams(term)
        trigram_matches = collections.defaultdict(int)
        for gram in termgram:
            matches = cls.product_index().get(gram, [])
            for match in matches:
                trigram_matches[match] += 1
        termgram_len = len(termgram)
        for match in trigram_matches:
            match_gram_len = cls.aka_index()[match][1]
            trigram_matches[match] = trigram_matches[match] / \
                (match_gram_len + termgram_len - trigram_matches[match])
        match_list = [(cls.aka_index()[k][0], k, v)
                      for k, v in trigram_matches.items()]
        match_list.sort(key=lambda el: el[2], reverse=True)
        return match_list[:5]

    @staticmethod
    def trigrams(term):
        """Return a list of trigrams for the provided term"""
        term = term.strip().lower()
        if len(term) < 3:
            return [term]
        i = 0
        results = []
        while i + 3 <= len(term):
            results += [term[i:i+3]]
            i += 1
        return results


def build_indexes(product_file):
    """ generate and return aka and trigram indexes """
    trigram_product_index = collections.defaultdict(set)
    aka_index = {}
    products = json.load(product_file)
    for name in products:
        if name.startswith('_'):
            continue
        name_trigrams = Trigram.trigrams(name)
        aka_index[name] = (name, len(name_trigrams))
        for trigram in name_trigrams:
            trigram_product_index[trigram].add(name)
        for aka in products[name].get('names', []):
            aka_trigrams = Trigram.trigrams(aka)
            aka_index[aka] = (name, len(aka_trigrams))
            for trigram in aka_trigrams:
                trigram_product_index[trigram].add(aka)
    # make trigram index json-compatible
    trigram_product_index = dict(trigram_product_index)
    for k in trigram_product_index:
        trigram_product_index[k] = sorted(list(trigram_product_index[k]))

    return aka_index, trigram_product_index