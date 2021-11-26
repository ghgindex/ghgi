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

## Amounts

Amounts have several different structures. The most common ones are:

* `QTY` `UNIT` -> "1 cup"
* `QTY` `UNIT` / `ALT_QTY` `ALT_UNIT` -> "1 cup/450ml"
* `QTY` `UNIT` (`ALT_QTY` `ALT_UNIT`) -> "1 cup (450ml)"
* `UNIT` -> "handful" (`QTY`=1 implicitly)
* `QTY` -> "2 scallops" (`UNIT`=`ea` implicitly)
* `None` -> "parmesan cheese" (`QTY`=1 or "standard", `UNIT`=`ea` or "per serving" implicitly)

Tricker ones typically provide clarifications of `each` amounts, in the following forms:

* `QTY` (`QTY` `UNIT`) `EA_UNIT` -> "1 (5 ounce) jar"
* `QTY` (`QTY`-`UNIT`) `EA_UNIT` -> "1 (5-ounce) jar"
* `QTY` `QTY`-`UNIT` `EA_UNIT` -> "1 5-ounce jar"
* `QTY` `QTY` `UNIT` `EA_UNIT` -> "1 5 ounce jar" which no one should write but we would parse the same way as above
* `QTY`-`UNIT` `EA_UNIT` -> "5-ounce jar"
* `QTY` `EA_UNIT` (`QTY` `UNIT` each) -> "3 salmon fillets (6oz each)"
* `QTY` `EA_UNIT` (`QTY` `UNIT`) -> "3 salmon fillets (18 ounces)" the qualifier is typically **total**, whether spelled out or not

For the above, if the qualifier is acting as an adjective to the unit, i.e. it occurs **before** the unit, it is a per-each qualifier. If it occurs after, it is a per-total qualifier, unless called out explicitly as per-each or using singular units.

We can identify qualifiers by looking for an amount or amounts that are sandwiched between a `QTY` and a `UNIT`.

Sometimes we get unit variants:

* `UNIT` or `UNIT` -> "can or jar"; these should be coalesced to the first of the list as `('can', 'UNIT')`

Some amounts are additive:

* `QTY` `UNIT` plus `QTY` `UNIT` item -> "1 cup plus 2 tablespoons flour"; the second item should be a `PLUS_AMT`.

There can also be prep adjectives between `QTY` and `UNIT`:

* `QTY` `PREP` `UNIT` -> "1 heaping cup"; this should convert to `[[(1, 'QTY'), ('cup', 'UNIT'), [mods]], 'AMT']`

And finally (?), sometimes you get multiple ingredients on a line, usually as alternatives:

* `QTY` `UNIT` name or `QTY` `UNIT` name -> "1 cup beans or 1/2 pound asparagus, trimmed"
* `QTY` `UNIT` name and `QTY` `UNIT` name -> "1 pound beef and 1/2 pound sausage"

We can identify these by (`AMT`, `NN*`) tuples separated by `and` or `or`
The latter of those bricks our current schema :grimacing:, but that isn't a problem for the parser to deal with.

Once this recoding is done, what remains is the "what" of the ingredient. We can strip out gerund clauses and so forth and should be on our way. With the possible exception of effing "grape or cherry tomatoes", which might just require an explicit workaround.

## Quantities

I think we might replace our regexes with a more bottom-up appoach. We could label numbers as a start, and from there label quantities, and from there identify which quantities are actually qualifiers.

## Qualifiers and Alternatives

Qualifiers and alternatives are similar, in that they interact with a precedent amount.

1. A qualifier clarifies the size of a precendent `ea` unit, usually indicated by either hyphenation, e.g. 1-pound, or parentheses, e.g. (1 pound), or sometimes both, e.g. (1-pound). It can also be indicated by markers like `about`, or `approx*`. A qualifier refers to the per-`ea` value, so it should be multiplied through unless indicated otherwise by a marker like `total`.
2. An alternative provides a measure for a different mass or volumetric unit (e.g. an amount in grams), usually indicated by a slash separating two units, e.g. 1 pound/454 grams, or parentheses, e.g. 1 pound (454 grams)

If we find an ALT_AMOUNT, we should look back in the ingredient to find the preceding AMOUNT, and append the ALT_AMOUNT to the AMOUNT's tokens. If the ALT_AMOUNT was preceded by a "/", we should remove that. If it was in a parenthetical, remove the parenthetical and any residual contents after we've made sure that all the ALT_AMOUNTS it contained have been moved into the precedent AMOUNT.

## Implicit (unitless/unquantified) Amounts

Sometimes, parts of amounts are specified implicitly, or not at all, e.g. "handful basil" (U but no Q; Q=1), "1 carrot" (Q but no U; U=each), or "chopped nuts" (neither!).

There are two ways this typically arises: either the UNIT is an implicit `ea` unit, e.g. `1 whole salmon`, or the QUANTITY is an implicit `1`, e.g. `handful dried parsley`. If we find a partial amount, we should scan forward to match it with its missing partner, stopping if we encounter a fully qualified amount which means we've moved on to something else. If we find its missing partner, we should move its token next to its precedent and label the pair as an AMOUNT. If we do not locate its missing partner, we should combine it with the default for its missing partner, either `ea` or `1`.

If the entire entry contains no AMOUNT, we should prepend an amount of `1 per`. `per` is a special case of `ea` which indicates that the actual amount wasn't provided, and it might need to be scaled based on servings or other considerations.

## Lists

One of the precipitating challenges of this approach is lists of alternatives, e.g. "grape or cherry tomato", "pinto, kidney, or lima beans"

## Ranges

Sometimes we get ranges: 1 to 2 cups, or 8 ounces to 1 pound.

## Compounds

Sometimes we get compound amounts, e.g. 1 pound plus 2 tablespoons

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
