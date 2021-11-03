# Ye Olde ToDo list

There is an issue if a recipe entry is blank, see e.g. this one [https://ghgi.org/admin/recipe/details/?id=31743]; we should just omit those.

Update the repo readme
Create package documentation
Flag products with no origin or food value information in validate
Validate that food_values are ok, e.g. "pd" has to be less than 1.0, "ed" > 1, etc.
Fix/improve how we're handling qualifiers that are in ounces, which a) probably means fluid ounces (?) and b) mean that the sg needs to be adjusted. See [https://www.seriouseats.com/is-there-a-ratio-for-converting-between-dried] for some data points.
- Make sure pydoc runs adequately

## Catalog

bread "loaf" vs "slice"?
diff between crackers and bread? (sugar, shortening, ?)
chile sauce/hot sauce, chili paste

## Note to self

Preserve commas when we remove stopwords! Otherwise you can end up with nonsense phrases.

Strip out `to`s at the end
replace `or`s with commas at the end

- certain uses of `or` are problematic when replaced by commas, e.g. `grape or cherry tomatoes` -> `['grape', 'cherry tomatoes']` or `cheese or potato pierogies` -> `['cheese', 'potato pierogies']`. Basically if you have a noun that's a food being used as a modifier, it can end up getting matched once the `or` is replaced. In an ideal world, these would get resolved as [`grape tomatoes`, `cherry tomatoes`] and [`cheese pierogies`, `potato pierogies`]; in a less-ideal-but-still-better world, we'd just get the raw strings back, or strings with the `or` stripped but not replaced with a comma.

Why isn't the parenthetical getting stripped out of this? `Kosher salt (Diamond Crystal) and black pepper`

## Parser

Torn fresh herbs, such as mint, dill, cilantro or parsley, for serving -> `torn` isn't getting removed
I'd also like to handle `whole` as a modifier, similarly to `can`, `bunch` and related things that aren't inherently quantified.

Certain products have names that are parts of different food's names: for instance "grape" is also in "grape tomato" and those are most definitely not the same thing. Conversely, "tuna" is only used for, well, tuna. The matcher right now prefers *longer* matches, which is to work around this problem, so if "grape or cherry tomato" gets split to "grape", "cherry tomato" we'll take the longer one. I think what we actually want to do is have a flag on these ingredients that says, essentially, this could be a partial match and only then prefer the longer matches. kinda gross but... There's a test in test_product.test_lookup that is commented out that would cover this, to which I'd add that when we have a list of names as ["tuna", "chickpea", "white bean"] we should prefer tuna, which we currently do not! In an ideal world we'd be smarter about the phrase/clause structure, but barf.

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
shortening, margarine
co-products analysis of sugar types, if available
Cranberry sauce
Diamond Crystal
Pepitas (pumpkin seeds)
makrut lime wtf is that?
dried za’atar
cornstarch
lye water
pastry dough

## Testing

Tests
Organize docs

be more consistent about singularizing terms
