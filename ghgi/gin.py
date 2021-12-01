import json
import collections
from ghgi.datasets import master
import nltk

try:
    from .datasets import MASTER_PRODUCTS, MASTER_GIN_INDEX, MASTER_AKA_INDEX
except:
    from datasets import MASTER_PRODUCTS, MASTER_GIN_INDEX, MASTER_AKA_INDEX

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
    # 'green',  # greens?
    # 'orange', # oranges!
    'purple'
    'red',
    'white',
    'yellow',
}

# words that must match
MUST_MATCH = {
    'leaf'
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
    def query(cls, term: str):
        # TODO: this could be improved by making better use of the pos_tags
        # and semantics. We can get smarter about identifying different patterns,
        # e.g. [NN1, OR, NN2] -> pick one of the NNx, vs [NN1, OR, NN2, NN3] in which case
        # it could mean [NN1 NN3, OR, NN2, NN3] OR [NN1 OR NN2 NN3] and so on.
        # It also needs to deal with commas!

        # To match, a term must include *all* the tokens of a database item.
        # It can have extraneous tokens, but must not be missing any
        tokens = cls.tokenize(term)

        # don't match on uninformative singletons
        if len(tokens) == 1 and cls.lower(tokens)[0] in NO_SOLO:
            return None, None, 0.0, 0, 0

        # identify the locations of ORs
        or_indexes = [i for i in range(
            len(tokens)) if tokens[i].lower() == 'or']

        if not or_indexes:
            return cls.best_match(tokens)

        # otherwise, generate whatever variants make most sense based on the OR
        # structure, match each variant's tokens, and select the best one.
        return cls.or_match(tokens)

    @classmethod
    def or_match(cls, tokens):
        # this is pretty complicated. For now, we're implementing a few simple
        # patterns, but we can add to this over time.
        pos_tags = cls.pos_tag(tokens)
        or_chunks = []
        cur_chunk = []
        for tag in pos_tags:
            if tag[0] in ['or', ',']:
                if cur_chunk:
                    or_chunks += [cur_chunk]
                cur_chunk = []
            else:
                cur_chunk += [tag]
        if cur_chunk:
            or_chunks += [cur_chunk]

        if not or_chunks:
            return None, None, 0.0, 0, 0

        # First thing, match each chunk
        match_results = [cls.best_match([c[0] for c in chunk])
                         for chunk in or_chunks]
        max_match_pct = max([mr[2] for mr in match_results])
        candidates = [mr for mr in match_results if mr[2] == max_match_pct]
        candidates.sort(key=lambda el: el[3], reverse=True)
        return candidates[0]

    @classmethod
    def best_match(cls, tokens: list, use_keyword: bool = True):
        pos_tags = cls.pos_tag(tokens)
        # the keyword is the last noun: must match if use_keyword is True
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
                    if m in results:  # limit to keyword matches
                        results[m] += 1

        else:
            results = collections.defaultdict(int)
            for i, t in enumerate(stemmed_tokens):
                matches = cls.index().get(t, [])
                for m in matches:
                    results[m] += 1

        # filter for candidate matches that have *all* of their terms in the query
        full_matches = {}
        for r in results:
            stemmed_result_tokens = cls.stem(cls.tokenize(r))
            if all([srt in stemmed_tokens for srt in stemmed_result_tokens]):
                musts = [m for m in MUST_MATCH if m in stemmed_tokens]
                if musts:
                    if not all([m in stemmed_result_tokens for m in musts]):
                        continue
                full_matches[r] = results[r]

        results = full_matches

        if len(results) == 0:
            if use_keyword:
                # fall back to not matching on keyword
                return cls.best_match(tokens, use_keyword=False)
            else:
                return None, None, 0.0, 0, 0

        max_match_count = max([v for v in results.values()])
        max_matches = [k for k, v in results.items() if v == max_match_count]
        term_size = len(tokens)
        if len(max_matches) == 1:
            selected = max_matches[0]
            match_size = len(cls.tokenize(selected))
            match_pct = max_match_count*2 / (match_size + term_size)
            return selected, cls.aka_index()[selected], match_pct, match_size, term_size

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
                selected_size = match_size

        return selected, cls.aka_index()[selected], best_score, selected_size, term_size
