# Greenhouse Gas Index
[![](https://img.shields.io/badge/license-CC--BY--SA%204.0-blue)](https://creativecommons.org/licenses/by-sa/4.0/)

The Greenhouse Gas Index is a database of primary food products and their GHG impacts, and [Python APIs](#python-apis) for accessing that data. The raw data is also available in JSON format for use in languages other than Python.

The database is built and maintained by [The Greenhouse Gas Index Organization (GHGI)](https://ghgi.org), a not-for-profit organization whose mission is to reduce GHG emissions by driving individual behaviour change through increased awareness of the climate impact of our everyday choices. Derived from the most current peer-reviewed science, GHGI makes it simple for consumers to understand the climate impact of what they eat.

## [Python APIs](#python-apis)
Documentation to follow.

## Web API
The database is also freely accessible via a [web API](https://api.ghgi.org) along with [documentation](https://ghgi.org/api/docs).

## Datasets
The database contains three primary datasets:
* [Products](#products) (and product [indexes](#product-indexes)) includes food products and their associated names, nutritional values, and physical data
* [Origins](#origins) provides per-product, per-geography climate impact data as available from credible references
* [References](#references) includes the data sources cited by Origins

All units in the datasets are metric.

### In-memory Database
Because the dataset is quite small, and almost entirely read-only, it is packaged inline with the code base and meant to be served from memory, resulting in a highly performant service. There may come a point where the dataset becomes sufficiently large that populating a standalone database will be preferable, or at least desirable in some cases; we'll cross that bridge when we get to it.

### [Products](#products)
Products is a JSON collection of product names and data values as follows:
```
  {
    "carrot": {data},
    ...
  }
```

The data values themselves JSON collections structured as:
```
{
  "g": float, # standard weight in grams
  "sg": float, # specific gravity in grams/ml
  "pd": float, # (optional) protein density in ?/?
  "ed": float, # (optional) energy density in kJ/kg
  "super": { # (optional) constituent ingredients
    "super_1": float, # % (ratio?) of product that is super_1
    "super_2": float,
    ...
  },
  "loss": { # (optional) % of parents lost in processing
    "super_1": float # % loss of super_1
  },
  "names": { # collection to generate aliases from
    "name_1": { 
      "dependent": [ # modifiers that *must* be accompanied by the name
        "mod_1"
        "mod_2",
        ...
      ], ...
    },
    "name_2": {
      "independent": [ # modifiers that *may* be accompanied by the name
        "standalone_variant_1"
        "standalone_variant_1",
        ...
      ], ...
    }
  },
  "aliases": [str, str, ...], # other names for the product (generated from the `names` struct)

  # Food composition values
  "caf" float, # (optional) % of product that is a caffeine
  "coc" float, # (optional) % of product that is a cocoa
  "fv": float, # (optional) % of product that is a fruit or vegetable
  "of": float, # (optional) % of product that is an oil fat
  "m": float, # (optional) % of product that is a milk or milk substitute
  "r": float, # (optional) % of product that is a root vegetable
  "s": float, # (optional) % of product that is a sugar
}
```

### [Product Indexes](#product-indexes)
Products are indexed in two ways: aliases (name variants) are indexed to their canonical product identifier, and a trigram index is generated across all name variants. The trigram index is crucial to parsing free-form ingredient lists, which frequently exhibit oddities even after pre-processing. Both of these indexes are JSON collections.

Alias index format:
```
  {
    "alias": [
      "canonical product name", 
      n_trigrams # number of trigrams in the alias
    ], ...
  }
```

Trigram index format:
```
  {
    "tri": [
      "alias_1",
      "alias_2",
      ...
    ], ...
  }
```

Combined, these two indexes make it very simple to match a text entry to the correct product regardless of how it is referenced.

### [Origins](#origins)
Origins is a JSON collection of origin information as follows:
```
  {
    "canada": {origin_info},
    ...
  }    
```

Each origin's information is a JSON collection of products available from that origin, their GHG impact, and the primary reference source for the impact data:
```
  {
    "canonical_product_name": [
      int, # reference id
      [
        ghg10(float), # ghg mass ratio @10th percentile
        ghgmean(float), # ghg mass ratio mean
        ghgmedian(float), # ghg mass ratio median
        ghg90(float), # ghg mass ratio @90th percentile
      ],
      str # (optional) text note
    ],
    ...,
    "super": "north america" # parent origin 
  }

```

Currently, for most products, we use the global origin as it has the most data available. While not yet implemented, Origins has been designed to allow for individual producers and regions as origins.

Further information about Origins is available [here](ghgi/datasets/master/origins).

### [References](#references)
References are a JSON collection whose keys are reference IDs whose values include pertinent metadata for that reference:
```
  {
    "1": {
      "authors": str, # list of authors
      "date": str, # publication date formatted as 2000-01-01
      "publication": str, # primary publication, e.g. Science
      "publication_info": str, # additional publication information, e.g. Volume, Issue, and page references
      "title": str, # article title
      "notes": str, # (optional) internal usage notes
      "url": str # url for the article or source
    },...
  }
```

## Contributing
We welcome pull requests, especially in the following areas:
* Additions or changes to the master products, origins, and references datasets
* Localizations of the master datasets
* Improvements to the Python APIs
* APIs for other languages

_Detailed instructions about contributing content or localizations to the datasets will follow._

Please note that additions or changes to the reference datasets require reference citations for any materially new information. Citations must reference recent, top-tier, peer-and/or-government-reviewed scientific publications.

## Attribution
This codebase is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/). If you make use of the database, please make sure to appropriately credit GHGI as the source of your data. To help build a standard, open, central, canonical resource for GHG food data, we also strongly encourage contributing incremental data directly to this repository (as opposed to forking).

Additionally, if you are using GHGI in a public product, please let us know so we can feature you here.
