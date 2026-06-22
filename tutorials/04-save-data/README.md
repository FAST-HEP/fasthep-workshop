# Save data

The previous tutorials worked directly on CMS Open Data NanoAOD files.

In many HEP analyses, this is not how the bulk of the analysis is performed. Instead, the first step is often to create a **skim**: a smaller dataset containing only the events and quantities needed for a particular study.

Skims reduce storage requirements, improve processing performance, and make it easier to move datasets between computing facilities, local clusters, and laptops.

FAST-HEP is designed to make this process simple and reproducible. Any quantity present in the event stream can be written out, including:

* original dataset branches
* analysis-facing field mappings
* derived quantities
* event selections

This allows skims to be described declaratively alongside the rest of the analysis workflow.

The tutorials in this section demonstrate:

* creating skims from larger datasets
* reducing datasets to only the columns needed for an analysis
* preserving provenance information so saved datasets remain traceable

Together, these features make it possible to move from experiment-produced data to compact, analysis-specific datasets while keeping the workflow reproducible and easy to share.

* [creating skims](04-save-data/01-skims)
* [selecting output columns](04-save-data/02-column-selection)
* [tracking provenance](04-save-data/03-provenance)

```{toctree}
:maxdepth: 1
:hidden:

04-save-data/01-skims
04-save-data/02-column-selection
04-save-data/03-provenance
```
