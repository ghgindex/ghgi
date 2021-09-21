import json
import collections
import nltk

from .datasets import MASTER_PRODUCTS, MASTER_GIN_INDEX, MASTER_AKA_INDEX

# words to exclude from stemming
NO_STEM = {
    'whiting'
}

# words that cannot be matched on their own
NO_SOLO = {
    'black',
    'blue',
    'grey',
    'gray',
    'green',  # greens?
    # 'orange', # oranges!
    'purple'
    'red',
    'white',
    'yellow',
}


class GIN:
    """ A GIN index optimized for matching ingredient entries.
    """

    _stemmer = None
    _index = None
    _aka_index = None

    @classmethod
    def index(cls):
        if not cls._index:
            with open(MASTER_GIN_INDEX) as p:
                cls._index = json.load(p)
        return cls._index

    @classmethod
    def aka_index(cls):
        if not cls._aka_index:
            with open(MASTER_AKA_INDEX) as p:
                cls._aka_index = json.load(p)
        return cls._aka_index

    @classmethod
    def stemmer(cls):
        if cls._stemmer is None:
            cls._stemmer = nltk.SnowballStemmer('english')
        return cls._stemmer

    @classmethod
    def tokenize(cls, text: str) -> list:
        return nltk.word_tokenize(text)

    @classmethod
    def stem(cls, tokens: list) -> list:
        return [cls.stemmer().stem(t) if t not in NO_STEM else t for t in tokens]

    @classmethod
    def pos_tag(cls, tokens: list) -> list:
        return nltk.pos_tag(tokens)

    @classmethod
    def lower(cls, tokens: list) -> list:
        return [t.lower() for t in tokens]

    @classmethod
    def generate(cls):
        """ Generate and return the GIN index.

        The GIN index is a dictionary with stemmed tokens as keys and the
        list of product aliases they match as values.
        """
        with open(MASTER_PRODUCTS, 'r') as product_file:
            gin_index = collections.defaultdict(set)
            products = json.load(product_file)
            for name in products:
                if name.startswith('_'):
                    continue

                name_tokens = cls.lower(cls.tokenize(name))
                stemmed_tokens = cls.stem(name_tokens)
                for token in stemmed_tokens:
                    gin_index[token].add(name)

                for aka in products[name].get('names', []):
                    aka_tokens = cls.lower(cls.tokenize(aka))
                    stemmed_aka_tokens = cls.stem(aka_tokens)
                    for token in stemmed_aka_tokens:
                        gin_index[token].add(aka)

            # make gin index json-compatible
            gin_index = dict(gin_index)
            for k in gin_index:
                gin_index[k] = sorted(
                    list(gin_index[k]))

            return gin_index

    @classmethod
    def query(cls, term: str, use_keyword=True):
        tokens = cls.tokenize(term)

        # don't match on uninformative singletons
        if len(tokens) == 1 and cls.lower(tokens)[0] in NO_SOLO:
            return None, None, 0.0

        pos_tags = cls.pos_tag(tokens)
        # the keyword is the last noun: must match if use_keyword is set
        key_word_index = None
        if use_keyword:
            for i, el in enumerate(reversed(pos_tags)):
                if el[1].startswith('NN'):
                    key_word_index = len(pos_tags)-(i+1)
                    break
        stemmed_tokens = cls.stem(cls.lower(tokens))

        if key_word_index is not None:
            matches = cls.index().get(stemmed_tokens[key_word_index], [])
            results = {k: 1 for k in matches}
            for i, t in enumerate(stemmed_tokens):
                if i == key_word_index:
                    continue
                matches = cls.index().get(t, [])
                for m in matches:
                    if m in results:
                        results[m] += 1

        else:
            results = collections.defaultdict(int)
            for i, t in enumerate(stemmed_tokens):
                matches = cls.index().get(t, [])
                for m in matches:
                    results[m] += 1

        if len(results) == 0:
            if use_keyword:
                # fall back to not matching on keyword
                return cls.query(term, use_keyword=False)
            else:
                return None, None, 0.0

        max_match_count = max([v for v in results.values()])
        max_matches = [k for k, v in results.items() if v == max_match_count]
        term_size = len(tokens)
        if len(max_matches) == 1:
            selected = max_matches[0]
            match_size = len(cls.tokenize(selected))
            match_pct = max_match_count*2 / (match_size + term_size)
            return selected, cls.aka_index()[selected], match_pct

        # select from multiple candidate matches
        best_score = 0.0
        selected = None
        for match in max_matches:
            match_size = len(cls.tokenize(match))
            match_pct = max_match_count*2 / (match_size + term_size)
            if match_pct > best_score:
                # find the one that matched most closely as a share of its size
                best_score = match_pct
                selected = match
            elif match_pct == best_score and len(match) > len(selected):
                best_score = match_pct
                selected = match

        return selected, cls.aka_index()[selected], best_score
