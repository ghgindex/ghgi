# Recipe Grammar

Implicit in the parser (and subsequent name matching) is a *de facto* grammar. It would likely yield better results, be more straightforward to modify, adapt and evolve, and result in cleaner code if we actually structured it as such. I'm not yet sure exactly what form this will take, but I think it will be modeled on nltk's NLP grammar, and may even end up being a custom grammar in nltk.

## Current approach

Currently, the parser goes through the following steps:

* Prepare the input string:
  * removes leading "directives" (e.g. "For the garnish:")
  * strip out html tags
  * replace word numbers with numerals
  * parenthesize qualifiers such as "4-pound", "five-to-size pound"
  * ensure parentheticals have spaces at their beginning and end
  * expand unicode vulgar fractions
  * pad hyphenated ranges, e.g. "six-to-eight" -> "six to eight"
  * pad non-numerical slashes and commas with spaces
  * singularize nouns and remove stopwords
    * stopwords are from a fixed list
* Parse out ingredient quantities
  * using regexes, extract various quantity formats
  * remove the text that represented those quantities
* Further prepare the remainder
  * remove prepositional phrases ("on", "at", "in")
  * remove any remaining parentheticals
  * replace "or", "to", "plus" conjunctions with commas or spaces
  * remove any remnant units
* Parse out names and modifiers
  * modifiers are identified from a fixed list

Some of these are sensible as pre-processing steps, whereas other seem like artifacts resulting from how our regexes behave. In aggregate, however, we lose *a lot* of semantic value from this approach.

## NLP approach

The new flow, which will be able to use many (I hope) of the existing regexes, should go as follows:

1. Pre-process
   * Strip leading/trailing whitespace
   * Strip out any html tags
     * At some point, we need to decide the "correct" way to handle inlined recipe links and whether we want to do anything about that
   * Expand vulgar fractions, prepending a space, e.g. "1¼" -> "1 1/4" (nltk will take 1/4 as a number, huzzah!)
   * Convert fractional numbers to decimals (?)
   * What about concatenated units, e.g. "6c" -> convert those to "6 cup" here, or should that come later?
2. Disregard ingredients that:
   * end in a colon ":" as this almost always means it's a directive
     * There are a few cases where a quantity is provided as part of this, but this is very rare, and more often than not the quantity is redundant with subsequent entries. We'll live with the misses here.
   * begin with certain other directives, which typically include a colon, e.g. "Equipment:...", "Accompaniment:...", "Ingredient info:..."
   * are entirely parenthetical, e.g. "(Essential oil complement: orange)"
   * Things that are marked optional TBD
     * I lean towards ignoring these, too

* [Chunk](#chunking) the input line, in particular decomposing dual entries (qty1 of this, or qty2 of that)
  * The relationship between subsequent chunks should be specified as an AND or an OR (default OR)
* each chunk should be converted to an object with a quantity, any qualifiers, and its names and any stripped mods
  * chunk having multiple quantities should be *extremely* rare
  * in theory, we shouldn't care about the position of the quantities once we're done extracting them
    * we might care about the position of quantity sub-chunks, e.g. for qualifiers, until we have completed the parse

## Chunking

The highest level chunk is an ingredient, which is an item and a quantity (which in some cases is implicit); some ingredient lines have multiple ingredient chunks which we will separate out. We should also look to remove gerunds and prepositional phrases (e.g. across the grain, on the bias) and other indicators of preparation instructions vs ingredient info.

As we build up meta-chunks, one question is how we want to represent this. Maybe just a list of tuples that are [start_index, stop_index, POI, raw_text, value, sub_chunks]?

## Parts of Ingredients (POI, à la POS)

Our grammar needs parts of speech to describe different elements of an ingredient:

* AMT -> QTY, QUAL?, UNIT: amount (quantity and units, but not always both)
* QTY: quantity
* UNIT: unit
* QUAL: amount qualifier (e.g. 4-pound)
* NAME: name
* DIR: directive (e.g. chopped)
* CTX: context ("for the garnish", "packed in olive oil", "sliced across the grain")
* OTH: other

Can DIR and CTX be the same thing? The only case I can see for separating them is that certain directives might affect how we interpret the density, e.g. chopped onion vs pureed.

An amount can include a qualifier, e.g. "1 (5- to 6-ounce) can" means the QTY is 1, the unit is "can", and the qualifier is 5.5 ounces.

At minimum, an Ingredient must include an amount and a name. In some cases, the amount will be implicit, e.g. "salt and pepper", or "apple".

## Ingredient Structures

* `<A><N>`
* `<A><AQ><N>`
* `<A><D><N>`
* `<A><N><D>`
* `<A><AQ><N><D>`
* `<A><AQ><D><N>`

In some cases, multiple ingredients will occur in the same entry, particularly when an alternative is being provided, e.g. "1 (5- to 6-ounce) can or jar tuna, drained and flaked, or 1 (13-ounce) can chickpeas or white beans, drained". I think this is indicated by an "or" following a full ingredient entry and directly preceding another full ingredient entry

## Quantities

I think we might replace our regexes with a more bottom-up appoach. We could label numbers as a start, and from there label quantities, and from there identify which quantities are actually qualifiers.

## Lists

One of the precipitating challenges of this approach is lists of alternatives, e.g. "grape or cherry tomato", "pinto, kidney, or lima beans"

## Ranges

Sometimes we get ranges: 1 to 2 cups, or 8 ounces to 1 pound.

## Compounds

Sometimes we get compound amounts, e.g. 1 pound plus 2 tablespoons

## Implicit amounts

Sometimes, parts of amounts are specified implicitly, or not at all, e.g. "handful basil" (U but no Q; Q=1), "1 carrot" (Q but no U; U=each), or "chopped nuts" (neither!).

The grammar needs to handle this as well.

## NLTK Parts of Speech

CC: coordinating conjuction
CD: numeral
DT: determiner (any, all)
IN: preposition or subordinating conjunction
JJ: adjective
JJR: comparative adjective
JJS: superlative adjective
MD: model (e.g. can)
NN: singular noun
NNS: plural noun
NNP: proper noun
RB: adverb
RBR: as for JJ
RBS: as for JJ
VB: verb
VBD: verb past tense
VBG: gerund
VBN: verb past participle
VBP: verb present tense
VBZ: verb present tense 3rd person singular
