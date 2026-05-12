# Example Data

Examples should use public data or generated toy data.

Large ROOT files should not be committed directly. Prefer:

- a small generation script for toy examples
- a download script for public external datasets
- README links to public files

The tutorial split-package example uses `scripts/ci/make_tutorial_data.py` to generate a tiny local ROOT file. The runtime smoke example uses an in-repo toy source helper so public CI can run without network or external data.
