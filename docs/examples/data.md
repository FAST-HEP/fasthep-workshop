# Example Data

Examples should use public data or generated toy data.

Large ROOT files should not be committed directly. Prefer:

- a small generation script for toy examples
- a download script for public external datasets
- README links to public files

The testing split-package workflow uses `scripts/ci/make_testing_data.py` to
generate a tiny local ROOT file. The runtime smoke workflow uses an in-repo toy
source helper so public CI can run without network or external data.
