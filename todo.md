# Ye Olde ToDo list

Update the repo readme
Create package documentation

- Make sure pydoc runs adequately

verify densities w/r/t FAO/INFOODS

## Catalog

ice cream
bread "loaf" vs "slice"?

## Note to self

Preserve commas when we remove stopwords! Otherwise you can end up with nonsense phrases.

Strip out `to`s at the end
replace `or`s with commas at the end

- certain uses of `or` are problematic when replaced by commas, e.g. `grape or cherry tomatoes` -> `['grape', 'cherry tomatoes']` or `cheese or potato pierogies` -> `['cheese', 'potato pierogies']`. Basically if you have a noun that's a food being used as a modifier, it can end up getting matched once the `or` is replaced. In an ideal world, these would get resolved as [`grape tomatoes`, `cherry tomatoes`] and [`cheese pierogies`, `potato pierogies`]; in a less-ideal-but-still-better world, we'd just get the raw strings back, or strings with the `or` stripped but not replaced with a comma.

Why isn't the parenthetical getting stripped out of this? `Kosher salt (Diamond Crystal) and black pepper`

## Parser

Torn fresh herbs, such as mint, dill, cilantro or parsley, for serving -> `torn` isn't getting removed
I'd also like to handle `whole` as a modifier, similarly to `can`, `bunch` and related things that aren't inherently quantified.

### Each types

- rib(s) - this is a hard one as it conflicts with animal ribs

### Sneaky words

## Match errors

We also might want to strip out adverbs!

### Efficiency ratios

We need to make sure that these are being calculated correctly given parent items. This should work the same way as it does for recipes: calculate the efficient value for each constituent, and divide the total impact of the ingredient by the sum of that.

Verify that the chicken (and other) stock super percents are right

Decide what to do with `LOSS`

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
co-products analysis of sugar types, if available
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
