# Read data

In the previous tutorial you ran a complete FAST-HEP workflow using a built-in toy data source.

FAST-HEP can work with many kinds of data sources. A workflow may read local files, access remote datasets, generate synthetic data, query databases, or use custom adapters provided by users and experiments.

In this workshop we will focus on High Energy Physics analysis workflows. In practice, this means working primarily with ROOT files containing event data.

Most tutorials use public datasets from the CMS experiment available through CERN Open Data. These datasets are freely accessible and provide realistic analysis examples without requiring experiment membership or credentials.

The following tutorials introduce the main concepts involved in reading data:

- [reading ROOT files](01-read-data/01-root-files)
- [organising inputs into datasets](01-read-data/02-datasets)
- [accessing data remotely](01-read-data/03-remote-data)

```{toctree}
:maxdepth: 1
:hidden:

01-read-data/01-root-files
01-read-data/02-datasets
01-read-data/03-remote-data
```
