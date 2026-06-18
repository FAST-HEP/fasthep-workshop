# Summarise data

Once data has been transformed into the quantities needed for an analysis, the next step is to summarise it.

In High Energy Physics, this is most commonly done using **histograms** and **tables**. Histograms provide compact representations of large datasets, while tables are often used to summarise event counts, selections, and cutflows.

FAST-HEP builds on the [boost-histogram](https://boost-histogram.readthedocs.io/) ecosystem for histogramming and uses [Matplotlib](https://matplotlib.org/) together with [mplhep](https://mplhep.readthedocs.io/) for visualisation.

FAST-HEP currently supports:

* one-dimensional histograms
* two-dimensional histograms
* weighted and unweighted histogram filling
* cutflow and summary-table outputs

When filling histograms, FAST-HEP automatically tracks datasets as a separate axis. This allows multiple datasets to be accumulated independently and combined later during rendering.

The rendering system uses mplhep to provide familiar High Energy Physics plotting styles while remaining fully configurable.

The following tutorials introduce the most common summarisation workflows:

* [creating histograms](03-summarise-data/01-histograms)
* [rendering histograms](03-summarise-data/02-render-histograms)
* [working with two-dimensional histograms](03-summarise-data/03-two-dimensional-histograms)
* [creating cutflow tables](03-summarise-data/04-cutflow-tables)

```{toctree}
:maxdepth: 1
:hidden:

03-summarise-data/01-histograms
03-summarise-data/02-render-histograms
03-summarise-data/03-two-dimensional-histograms
03-summarise-data/04-cutflow-tables
```
