# Product source dataset

Products is the master database of product metadata. Each entry is keyed under its canonical name, typically driven by the source data it is pulled from. Each entry's dictionary includes its metadata:
 * `g` (float) standard weight in grams
 * `sg` (float) specific gravity in grams/ml ref H2O
 * `pd` (float) (optional) protein density in ?/?
 * `ed` (float) (optional) energy density in kJ/kg
 * `super` (dict) (optional) constituent ingredients
    * `super_1` (float) % (ratio?) of product that is super_1
    * `super_2` (float)
    * ...
 * `loss` (dict) (optional) % of supers lost in processing
    * `super_1` (float) % loss of super_1
    * ...
* `names` (dict) (optional) see [Name Variations](#name-variations) below

### [Name Variations](#name-variations)
Most products are known by multiple names, whether because an identical product goes by multiple names, or has multiple variants, or because a group of products are functionally equivalent. To help with this, we employ a `names` structure in the products source file that enables us to consistently generate variant combinations. Each key in the `names` dictionary is another name the master product is known by; each will be included as a name for the master product.

Each entry in the `names` dictionary may also optionally include two different types of modifiers: `dependent` and `independent`. Dependent modifiers are found *only in combination with* the parent name, whereas independent modifiers can appear with or without it. In the context of "apple", "green" is a dependent modifier, but Granny Smith is independent. By default the variant **precedes** the main name; for trailing modifiers, prefix the name with an underscore. To remove the space, preface the variant with a `.`, which can be combined with `_` to add a trailing space-less modifier.

In some cases, names are duplicated: most notably in the case of wild vs farmed seafood. In this case the predominant form of the product will take its generic name, e.g. "trout", and the less common form will only be identified explicitly, e.g "wild trout". To facilitate this, base names may be prefaced with `~` to indicate that they are **not** standalone.

For a `names` entry with no further variants, simply set its value to an empty dictionary `{}`.

Finally, do not worry about possible duplication; the script that generates the master database from the source file ensures that all names are uniqued within a product, and that the resulting names are unique across all products.

An example `names` dictionary for apples:
```
{
    "apple": {
        "dependent": ["green", "red", "_of the ozarks"],
        "independent": ["granny smith", "mcintosh"]
    }
}
```

This would result in the following list of aliases for "apple":
 * apple
 * green apple
 * red apple
 * apple of the ozarks
 * granny smith apple
 * granny smith
 * mcintosh apple
 * mcintosh

It should be noted that as far as I'm aware the "apple of the Ozarks" is not a thing.