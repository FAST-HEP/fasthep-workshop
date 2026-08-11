# Explicit dependencies with `needs`

Analysis stages have an implicit dependency on the previous stage by default.
This is convenient for simple sequential workflows, where authors do not need
to write every dependency explicitly.

Not every analysis is a serial chain, however. The `needs` field can override
this implicit ordering to expose independent branches explicitly.

This tutorial builds the following workflow:

```{mermaid}
flowchart LR
    Source["<b>read.events</b>"]:::source
    Prepare["<b>Prepare</b>"]:::transform
    BranchA["<b>BranchA</b>"]:::transform
    BranchB["<b>BranchB</b>"]:::transform
    Combine["<b>Combine</b>"]:::transform
    Audit["<b>IndependentAudit</b>"]:::transform

    Source --> Prepare
    Prepare --> BranchA
    Prepare --> BranchB
    BranchA --> Combine
    BranchB --> Combine

    Source --> Audit
```

`Prepare` uses the default behaviour because it has no `needs` key. `BranchA`
and `BranchB` both explicitly depend on `Prepare`, making them independent
siblings rather than a sequential `BranchA → BranchB` chain. `Combine` depends
on both branches.

`IndependentAudit` uses `needs: []`, suppressing the implicit dependency on the
previous analysis stage entirely.

The three forms are:

```yaml
# implicit dependency on the previous stage
- id: B
  op: ...
```

```yaml
# explicit dependency on stage A instead
- id: B
  op: ...
  needs: [A]
```

```yaml
# no stage-ordering dependency
- id: B
  op: ...
  needs: []
```

`needs` refers to analysis stage ids and expresses **ordering dependencies**. It
replaces only the implicit dependency on the previous analysis stage.

Other dependencies are unaffected. Operation specifications, `from` bindings,
source bindings, and parameter-derived field requirements still contribute to
the compiled graph.

## `needs` and `from`

`needs` does not select an output product or bind an input port. Use `from`
when an operation consumes a concrete upstream product.

In this tutorial, the branch stages use `from` to select the stream produced by
`Prepare`, while `needs` expresses their stage-ordering relationship:

```text
from
    which product does this operation consume?

needs
    which analysis stages must precede this stage?
```

Keeping these concepts separate allows Flow to reason independently about data
flow and stage ordering.

## Run the workflow

From the repository root:

```bash
pixi run fasthep run tutorials/06-organise-workflows/02-needs/workflow.yaml \
  --outdir build/tutorials/06-organise-workflows/02-needs
```

The main output to inspect is the compiled graph:

```text
build/tutorials/06-organise-workflows/02-needs/graph/graph.svg
```

Alternative graph representations are also available:

```text
graph/graph.mmd
graph/graph.d2
graph/graph.dot
```

The graph should show that:

* `Prepare` follows the input source
* `BranchA` and `BranchB` both follow `Prepare`
* neither branch depends on the other
* `Combine` depends on both branches
* `IndependentAudit` starts from the input source and does not depend on
  `Combine`

The resulting workflow is therefore branched rather than the sequential chain:

```text
Prepare → BranchA → BranchB → Combine
```
