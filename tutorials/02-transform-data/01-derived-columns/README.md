# Derived columns

> Part 1 of 3 in **Transform Data**
>
> ▶ 01. Derived Columns  
> ○ 02. Object Selections  
> ○ 03. Project Fields

This tutorial reads the small local Z &rarr; $\mu\mu$ ROOT files and adds a few
derived quantities to the event stream.

It does not make histograms, skim files, run systematics, or use distributed
execution. The output to inspect is the schema report before and after the
transform.

## 1. Inspect the dataset file

Datasets live in `datasets.yaml`:

```yaml
datasets:
  data:
    files:
      - data/CMS/Zmumu/data.root
  dy:
    files:
      - data/CMS/Zmumu/dy.root
```

The data files are the same small files used by the read-data tutorials.

## 2. Inspect the transform

`author.yaml` adds fields with `hep.define`:

```yaml
analysis:
  stages:
    - id: DerivedMuonColumns
      op: hep.define
      params:
        variables:
          - name: Muon_Pt
            expr: "sqrt(Muon_Px ** 2 + Muon_Py ** 2)"
```

The same stage also defines an isolated-muon mask:
```yaml
- name: IsolatedMuon
  expr: "(Muon_Iso / Muon_Pt) < 0.10"
```
and counts isolated muons per event:
```yaml
- name: NIsolatedMuon
  reduce:
    op: count_nonzero
    over: IsolatedMuon
```

These three variables, `Muon_Pt`, `IsolatedMuon`, and `NIsolatedMuon`, are then available to later stages.

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/02-transform-data/01-derived-columns/author.yaml --outdir build/tutorials/02-transform-data/01-derived-columns
```

## 4. Inspect the outputs

Look at:

- `build/tutorials/02-transform-data/01-derived-columns/compile/normalized.yaml`
- `build/tutorials/02-transform-data/01-derived-columns/compile/plan.yaml`
- `build/tutorials/02-transform-data/01-derived-columns/reports/schema/`
- `build/tutorials/02-transform-data/01-derived-columns/run_summary.yaml`

The schema snapshots show where the new derived fields enter the stream.

---

## Next steps

Next: {doc}`02. Object Selections </tutorials/02-transform-data/02-object-selections>`
