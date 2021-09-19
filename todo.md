# Ye Olde TODO list

## Note to self

The parser now successfully looks for interstitial parentheticals between the qty and the units! These are then parsed, and `quantify` infers all kinds of nice things if it receives an interstitial parenthetical.

Preserve commas when we remove stopwords! Otherwise you can end up with nonsense phrases.

Strip out `to`s at the end
replace `or`s with commas at the end
replace `plus` with comma

Why isn't the parenthetical getting stripped out of this? `Kosher salt (Diamond Crystal) and black pepper`
`1 packed cup cilantro, coarsely chopped`

## How to quantify with the new styles

We now can receive a qualifier for a quantity, which means there was a parenthetical or its equivalent near the entry. We can also receive multiple qty entries, which in some cases can be used to infer things. Finally, we are (or should be) getting correctly parsed data throughout the whole ingredient line.

With that info:
if the first qty entry is a `ea` or something similar, we multiply its quantity by either a) its qualifier's value IF the qualifier is a non-`ea` value, or b) subsequent qtys' value IF it's a non-`ea` value. If those fail, we default to the Product.mass value we have.

I'd also like to handle `whole` as a modifier, similarly to `can`, `bunch` and related things that aren't inherently quantified.

## Parse errors

`python3 setup.py test -s ghgi.tests.test_origin.TestOrigin.test_origin_entries`

### Each types

- rib(s) - this is a hard one as it conflicts with animal ribs

### Sneaky words

#### Additions

- 2 cups **plus** 1 tablespoon

## Match errors

The trigram index doesn't make sense. While it's likely better at dealing with misspellings, it's way too loose in its matches. I think we want to require full matches across stemmed tokens. Essentially, this is going to be a GIN index. When we get a query, we stem and tokenize it, and then query the GIN index with the tokens. "Matchiness" is derived by looking at how many of the tokens each candidate entry matches. We will also identify which token is the last noun, and *require* that to match.

## Mods

Some mods are problematic, e.g. fresh, when they conflict with key ways to separate out similar ingredients. For instance, 1 cup beans is quite different from 1 cup of fresh beans. We need to figure out a way to handle this, for both Mods and Stopwords. If you run test_stopword_safety and test_mod_safety if will squawk the offenders.

Also, we are stripping out `can` as a stopword, as it's also a unit. We need a test that makes sure there's no overlap between stopwords/prep mods and units!!

## Stopwords

## Missing things

Coconut, coconut milk, coconut oil
grapeseed oil
allspice
Add a general "seasoning" match which aliases to salt and pepper
Stuffing (use this as an alias for bread)
Cranberry sauce
Kosher Salt
Diamond Crystal
Pepitas (pumpkin seeds)
Tortilla
Plantains
Scotch bonnet pepper
makrut lime wtf is that?
sun-dried tomato
vanilla ice cream
sweet freestone peach
Turbinado sugar
maple syrup
dried za’atar
golden syrup
cornstarch
lye water
garam masala
turmeric
cayenne
cotija
onion powder

## Testing

Tests
Organize docs

be more consistent about singularizing terms

√ generate the full products.json file from the new product master and compare to the old one
remove sanity and products_original once happy
is this done? ^