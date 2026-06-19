# Transform data

You can now read data into a FAST-HEP workflow. The next step is to derive new quantities and select the events and objects relevant to your analysis.

Most High Energy Physics datasets are naturally represented as **columnar data**. Rather than looping over events one-by-one, analyses operate on columns of quantities such as particle momenta, energies, and identification flags.

Many of these quantities are also **jagged**: one event may contain two muons, another five, and another none at all.
FAST-HEP builds on the [Awkward Array](https://awkward-array.org/doc/main/) and [NumPy](https://numpy.org/doc/stable/) ecosystems, allowing workflows to operate naturally on variable-length collections using familiar array-oriented expressions.

All available quantities can be referenced by name. As workflows grow, it is often useful to map dataset-specific branch names onto stable analysis-facing field names, or derive new variables with more meaningful names.

FAST-HEP also provides a number of convenience functions for working with irregular event data, including operations such as selecting leading objects, handling missing values, and accessing specific entries within variable-length collections.

The following tutorials introduce the most common transformation operations:

- [deriving new quantities](02-transform-data/01-derived-columns)
- [selecting objects and events](02-transform-data/02-object-selections)
- [mapping dataset fields](02-transform-data/03-field-mapping)

```{toctree}
:maxdepth: 1
:hidden:

02-transform-data/01-derived-columns
02-transform-data/02-object-selections
02-transform-data/03-field-mapping
```
