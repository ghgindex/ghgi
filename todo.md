# Ye Olde ToDo list

Update the repo readme
Create package documentation
Make sure pydoc runs adequately
verify densities w/r/t FAO/INFOODS

## Catalog

ice cream
bread "loaf" vs "slice"?

## Note to self

The parser now successfully looks for interstitial parentheticals between the qty and the units! These are then parsed, and `quantify` infers all kinds of nice things if it receives an interstitial parenthetical.

Preserve commas when we remove stopwords! Otherwise you can end up with nonsense phrases.

Strip out `to`s at the end
replace `or`s with commas at the end

Why isn't the parenthetical getting stripped out of this? `Kosher salt (Diamond Crystal) and black pepper`
`1 packed cup cilantro, coarsely chopped`

## How to quantify with the new styles

We now can receive a qualifier for a quantity, which means there was a parenthetical or its equivalent near the entry. We can also receive multiple qty entries, which in some cases can be used to infer things. Finally, we are (or should be) getting correctly parsed data throughout the whole ingredient line.

With that info:
if the first qty entry is a `ea` or something similar, we multiply its quantity by either a) its qualifier's value IF the qualifier is a non-`ea` value, or b) subsequent qtys' value IF it's a non-`ea` value. If those fail, we default to the Product.mass value we have.

I'd also like to handle `whole` as a modifier, similarly to `can`, `bunch` and related things that aren't inherently quantified.

## Parser

Torn fresh herbs, such as mint, dill, cilantro or parsley, for serving -> `torn` isn't getting removed

### Each types

- rib(s) - this is a hard one as it conflicts with animal ribs

### Sneaky words

#### Additions

## Match errors

We also might want to strip out adverbs!

### Efficiency ratios

We need to make sure that these are being calculated correctly given parent items. This should work the same way as it does for recipes: calculate the efficient value for each constituent, and divide the total impact of the ingredient by the sum of that.

Verify that the chicken (and other) stock super percents are right

**Add a test to ensure that no products have more than one food category set!!**

Decide what to do with `LOSS`

something's up with dark chocolate -> it keeps getting an efficiency rating when it shouldn't

## Mods

Some mods are problematic, e.g. fresh, when they conflict with key ways to separate out similar ingredients. For instance, 1 cup beans is quite different from 1 cup of fresh beans. We need to figure out a way to handle this, for both Mods and Stopwords. If you run test_stopword_safety and test_mod_safety if will squawk the offenders.

Also, we are removing `can` from stopwords, as it's also a unit. We need a test that makes sure there's no overlap between stopwords/prep mods and units!!

## Stopwords

## Missing things

Condensed milk

Coconut, coconut milk, coconut oil
  Feraldi et al. (2012). Life Cycle Assessment of Coconut Milk and Two Non-Dairy Milk Beverage Alternatives. Franklin Associate
  Audsley et al. 2009
  Egads there is almost no research on this. We could use an estimate, but that's pretty gross.
  No sir; we'll just use a non-sourced entry! Which then spits out a null impact, which the site flags!

grapeseed oil
sesame seeds, sesame oil
allspice
Add a general "seasoning" match which aliases to salt and pepper
Cranberry sauce
Diamond Crystal
Pepitas (pumpkin seeds)
makrut lime wtf is that?
vanilla ice cream
sweet freestone peach
maple syrup
dried za’atar
cornstarch
lye water
garam masala
turmeric
pastry dough

## Testing

Tests
Organize docs

be more consistent about singularizing terms

√ generate the full products.json file from the new product master and compare to the old one
remove sanity and products_original once happy
is this done? ^