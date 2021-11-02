# Origins

Origins are, unsurpisingly, the places where products originate from. These are typically geographies, but can also be individual producers.

Each origin's data is a dictionary whose keys are products' canonical names, and whose values are tuples of:

- [`reference_id`, ...]
- [`ghg10`, `ghgmean`, `ghgmedian`, `ghg90`]
- optional note

## GHG Values

The `ghg` values are mass ratios of output_C02e:input. For instance, apples produce median GHG emissions of 0.42kg CO2e per kg of apples, so their `ghgmedian` value is 0.42. The largest single source of this data is Poore & Nemecek; these ghg values are found in this [supplemental](https://www.science.org/doi/suppl/10.1126/science.aaq0216/suppl_file/aaq0216-poore-sm-revision1.pdf) material.

For certain foods not covered by Poore & Nemecek, we have sourced this information elsewhere. The references are documented via `reference_ids`, and the optional note may include a link to a spreadsheet detailing how any necessary calculations were done. Many of the products calculated this way have the same value for each of the ghg entries because the source only provides a single value.

## Reference Ids

`reference_id` is our local id for the primary reference source(s) for the data.

The highest-level origin is the **global** origin, which is also the most commonly cited. Sub-origins (any origin other than Global) must cite a single `super` property, which is their parent origin. The parent origin is used as a fallback for data missing from a given non-global region.

For example, a tomato producer "ACME Tomatoes" located in Walla Walla, Washington would have its own origin file containing a single entry for its tomatoes, and a `super` value of Washington State. Washington in turn might have a `super` of `usa`, which in turn has a `super` of `north_america`, which in turns points to `global`.

The use of a dictionary allows us to easily add protected keys to include metadata like geocodes, addresses, display names, and the like.

Origin names must not include any whitespace.

As the depth of the origins files grows, they should be kept in a directory structure such that each non-terminal level of the tree has its own directory, for example:

```text
/origins
    global.json
    /north_america
        north_america.json
        /canada
            /bc
            /...
        /usa
            /wa
            /or
            /...
        /mexico
```
