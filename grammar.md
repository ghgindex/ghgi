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

## Chunking

To follow

## Parts of Ingredients (POI, à la POS)

Our grammar needs parts of speech to describe different elements of an ingredient:

* AMT -> QTY, QUAL?, UNIT: amount (quantity and units, but not always both)
* QTY: quantity
* UNIT: unit
* QUAL: amount qualifier (e.g. 4-pound)
* NAME: name
* DIR: directive (e.g. chopped)
* CTX: context ("for the garnish", "packed in olive oil")
* OTH: other

Can DIR and CTX be the same thing? The only case I can see for separating them is that certain directives might affect how we interpret the density, e.g. chopped onion vs pureed.

An amount can include a qualifier, e.g. "1 (5- to 6-ounce) can" means the QTY is 1, the unit is "can", and the qualifier is 5.5 ounces.

At minimum, an Ingredient must include an amount and a name.

## Ingredient Structures

* `<A><N>`
* `<A><AQ><N>`
* `<A><D><N>`
* `<A><N><D>`
* `<A><AQ><N><D>`
* `<A><AQ><D><N>`

In some cases, multiple ingredients will occur in the same entry, particularly when an alternative is being provided, e.g. "1 (5- to 6-ounce) can or jar tuna, drained and flaked, or 1 (13-ounce) can chickpeas or white beans, drained". I think this is indicated by an "or" following a full ingredient entry and directly preceding another full ingredient entry

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

