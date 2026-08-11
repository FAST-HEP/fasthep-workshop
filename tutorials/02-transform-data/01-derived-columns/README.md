# Derived columns

> Part 1 of 3 in **Transform Data**
>
> ▶ 01. Derived Columns  
> ○ 02. Object Selections  
> ○ 03. Field Mapping

This tutorial reads the small local Z &rarr; $\mu\mu$ ROOT files and adds a few
derived quantities to the event stream.

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

`workflow.yaml` adds fields with `hep.define`.
The first derived quantity is the muon transverse momentum:

```{math}
p_T = \sqrt{p_x^2 + p_y^2}
```

In FAST-HEP expression syntax this becomes almost a direct translation:

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

The expression uses the same branch names that appear in the input data. It also follows NumPy-style syntax,
where `** 2` means “squared” and functions such as `sqrt(...)` act on whole arrays rather than single values

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
pixi run fasthep run tutorials/02-transform-data/01-derived-columns/workflow.yaml --outdir build/tutorials/02-transform-data/01-derived-columns
```

## 4. Inspect the outputs

This workflow does not list the input branches explicitly in the source.

Instead, FAST-HEP inspects the expressions in `hep.define`, works out which input quantities are needed, and includes those branches automatically.

In this tutorial, the derived fields require:

- `Muon_Px`
- `Muon_Py`
- `Muon_Iso`

You can see this in the compiler dependency output:

```
build/tutorials/02-transform-data/01-derived-columns/compile/deps.yaml
```

The workflow also writes schema snapshots before and after the define stage:

```
build/tutorials/02-transform-data/01-derived-columns/reports/schema/read_events/events__data__0.json
build/tutorials/02-transform-data/01-derived-columns/reports/schema/stage_DerivedMuonColumns/events__data__0.json
```

The first schema shows the stream read from the ROOT file. The second schema shows the stream after `DerivedMuonColumns` has run.

The important difference is that the stream now contains three additional fields:

- `Muon_Pt`
- `IsolatedMuon`
- `NIsolatedMuon`

## Expected outputs

### Inferred dependencies

The dependency snippet shows that FAST-HEP recorded the input quantities required by the derived expressions.

```{literalinclude} /_static/_generated/tutorials/02-transform-data/01-derived-columns/snippets/deps.yaml
:language: yaml
```
This is useful because analysis authors do not need to manually keep branch lists in sync with their expressions.
If a derived quantity uses a new input branch, FAST-HEP can include it automatically.

### Schema after the define stage

The schema after `DerivedMuonColumns` includes the newly created fields.
```{literalinclude} /_static/_generated/tutorials/02-transform-data/01-derived-columns/snippets/schema_after_define.summary.json
:language: json
```

Compare this with the source schema if you want to see exactly where the stream changes:

```bash
diff \
  build/tutorials/02-transform-data/01-derived-columns/reports/schema/read_events/events__data__0.json \
  build/tutorials/02-transform-data/01-derived-columns/reports/schema/stage_DerivedMuonColumns/events__data__0.json
```
