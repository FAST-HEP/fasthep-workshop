Great. I’d make `04-save-data/03-provenance` a **read-only inspection tutorial**: no new workflow concepts, just “the previous skim already produced provenance; here is how to inspect it.”

Suggested structure:

````md
# Provenance

> Part 3 of 3 in **Save Data**
>
> ✓ 01. Skims  
> ✓ 02. Column Selection  
> ▶ 03. Provenance

This tutorial shows how to inspect the provenance recorded for saved outputs.

FAST-HEP records provenance for produced artifacts so you can answer:

- which workflow node produced this file
- which input dataset and partition it came from
- which workflow, graph, and plan were used
- which software versions and execution environment were used

## 1. Run a skim workflow

Use the skim workflow from the previous tutorial:

```bash
pixi run fasthep run tutorials/04-save-data/02-column-selection/author.yaml \
  --outdir build/tutorials/04-save-data/03-provenance
````

## 2. Inspect the provenance summary

```bash
pixi run fasthep -q provenance summary build/tutorials/04-save-data/03-provenance
```

The summary reads:

```text
artifacts/provenance/manifest.json
```

and reports the artifacts recorded for this run.

## 3. Show provenance for one output file

```bash
pixi run fasthep -q provenance show \
  build/tutorials/04-save-data/03-provenance/artifacts/files/dimuon_candidates/data/0_0.root
```

This answers where the file came from, including the producer node, input partition, source file, workflow references, software versions, and execution environment.

## 4. Show the provenance graph

```bash
pixi run fasthep -q provenance graph \
  build/tutorials/04-save-data/03-provenance/artifacts/files/dimuon_candidates/data/0_0.root
```

The graph reconstructs the workflow path that produced the selected artifact.

It combines:

* `artifacts/provenance/manifest.json`
* `artifacts/provenance/execution.json`
* the artifact provenance record
* `graph/graph.json`

FAST-HEP does not duplicate the full graph inside every artifact record. Instead, provenance files contain links that can be combined to reconstruct the full lineage.

## 5. Inspect the files directly

Look at:

* `build/tutorials/04-save-data/03-provenance/artifacts/provenance/manifest.json`
* `build/tutorials/04-save-data/03-provenance/artifacts/provenance/execution.json`
* `build/tutorials/04-save-data/03-provenance/artifacts/provenance/records/`

The manifest is the entry point. It points to compact artifact records.

`execution.json` stores information shared by the run, such as workflow references, software versions, execution environment, and input partitions.

The individual records link each artifact to the node and partition that produced it.
