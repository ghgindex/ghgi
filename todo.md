# Ye Olde TODO list

## Note to self

The parser now successfully looks for interstitial parentheticals between the qty and the units! These are then parsed, and `quantify` infers all kinds of nice things if it receives an interstitial parenthetical.

## How to quantify with the new styles

We now can receive a qualifier for a quantity, which means there was a parenthetical or its equivalent near the entry. We can also receive multiple qty entries, which in some cases can be used to infer things. Finally, we are (or should be) getting correctly parsed data throughout the whole ingredient line.

With that info:
if the first qty entry is a `ea` or something similar, we multiply its quantity by either a) its qualifier's value IF the qualifier is a non-`ea` value, or b) subsequent qtys' value IF it's a non-`ea` value. If those fail, we default to the Product.mass value we have.

I'd like to see us flag whether a subsequent modifier appears to be for 'each', or 'total', e.g. 4 fish fillets, about 280 g total. That's not *super* hard to do, but I want to see what terms are used besides 'total' and 'each'. And plus I'm sick of the parser right now and this can wait.

I'd also like to handle `whole` as a modifier, similarly to `can`, `bunch` and related things that aren't inherently quantified.

## Parse errors

`python3 setup.py test -s ghgi.tests.test_origin.TestOrigin.test_origin_entries`

### Each types

- stick(s)
- rib(s)
- bunch
- can
- jar
- tin

We'd like a way to specify a default each size for things like jar, tin.

### Sneaky words

#### Midpoints - HUZZAH we do this

`to` and `or` might need some consideration, as they get used a lot in ways that might be helpful
e.g. Number to Number means a range, and we should pick that up and use the midpoint

- 3 **or** 4
- 6 **to** 8

#### Additions

- 2 cups **plus** 1 tablespoon

### Parentheticals HUZZAH

- 1 (9-ounce) item

## Match errors

## Mods

Some mods are problematic, e.g. fresh, when they conflict with key ways to separate out similar ingredients. For instance, 1 cup beans is quite different from 1 cup of fresh beans. We need to figure out a way to handle this, for both Mods and Stopwords. If you run test_stopword_safety and test_mod_safety if will squawk the offenders.

Also, we are stripping out `can` as a stopword, when it's also a unit. We need a test that makes sure there's no overlap between stopwords/prep mods and units!!

## Stopwords

## Missing things

Porgy (fish)
Add a general "seasoning" match which aliases to salt and pepper
Stuffing (use this as an alias for bread)
Cranberry sauce
Kosher Salt
Diamond Crystal
Pepitas (pumpkin seeds)

## Testing

Tests
Organize docs

be more consistent about singularizing terms

√ generate the full products.json file from the new product master and compare to the old one
remove sanity and products_original once happy
is this done? ^