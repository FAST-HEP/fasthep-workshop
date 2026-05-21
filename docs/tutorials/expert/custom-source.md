# Creating your own data source

use download from remote_data.json, e.g.
```
sources:
  downloads:
    kind: workshop.download_manifest
    manifest: remote_data.json
    destination: data
    force: false
```
