# FAST-HEP overview

## Workflows
FAST-HEP workflows start from an `workflow.yaml`, then compile to normalized workflow and execution-plan files.

```{mermaid}
flowchart TD

    subgraph Compile["Compilation and planning"]
        Author["workflow.yaml"]
        Profiles["profiles and registries"]
        Normalised["normalised workflow"]
        Dependency["dependency inference"]
        Plan["execution plan"]

        Author --> Normalised
        Profiles --> Normalised
        Normalised --> Dependency
        Dependency --> Plan
    end

    subgraph Execute["Runtime execution"]
        Runtime["runtime execution"]
        Outputs["artifacts and outputs"]

        Runtime --> Outputs
    end

    Plan --> Runtime
```

Implementation packages contribute functionality through registry profiles. The workshop examples show how flow, carpenter, curator, and render profiles combine in an workflow file.

## Packages
The FAST-HEP ecosystem is split into focused packages.

Each package owns a small part of the workflow stack and exposes functionality through public APIs, profiles, registries, or command-line tools.
```{mermaid}
flowchart LR

    Flow["<b>fasthep-flow</b><br/>workflow compilation<br/>and orchestration"]

    Curator["<b>fasthep-curator</b><br/>dataset inspection<br/>metadata and provenance"]

    Carpenter["<b>fasthep-carpenter</b><br/>analysis transforms<br/>histograms and cutflows"]

    Render["<b>fasthep-render</b><br/>plots, reports<br/>and rendering"]

    CLI["<b>fasthep-cli</b><br/>command-line interface"]

    Workshop["<b>fasthep-workshop</b><br/>tutorials, examples<br/>and training material"]

    Flow --> Carpenter
    Curator --> Carpenter
    Carpenter --> Render
    CLI --> Flow
    Workshop --> Flow
```


| Package | Purpose | Documentation | Git Repo | 
|---|---|---|---|
| `fasthep-flow` | Workflow compilation, planning, runtime orchestration | [API docs](https://fasthep-flow.readthedocs.io/en/latest/) | [FAST-HEP/fasthep-flow](https://github.com/FAST-HEP/fasthep-flow) |
| `fasthep-carpenter` | Analysis transforms, histogramming, awkward/ROOT processing | [API docs](https://fasthep-carpenter.readthedocs.io/en/latest/) | [FAST-HEP/fasthep-carpenter](https://github.com/FAST-HEP/fasthep-carpenter) |
| `fasthep-curator` | Dataset inspection, provenance, diagnostics, metadata | [API docs](https://fasthep-curator.readthedocs.io/en/latest/) | [FAST-HEP/fasthep-curator](https://github.com/FAST-HEP/fasthep-curator) |
| `fasthep-render` | Plotting, reports, rendering pipelines | [API docs](https://fasthep-render.readthedocs.io/en/latest/) | [FAST-HEP/fasthep-render](https://github.com/FAST-HEP/fasthep-render) |
| `fasthep-cli` | Unified command-line interface | [API docs](https://fasthep-cli.readthedocs.io/en/latest/) |  [FAST-HEP/fasthep-cli](https://github.com/FAST-HEP/fasthep-cli) |
| `fasthep-toolbench` | Shared utilities and lightweight tooling | [API docs](https://fasthep-toolbench.readthedocs.io/en/latest/)  |  [FAST-HEP/fasthep-toolbench](https://github.com/FAST-HEP/fasthep-toolbench) |
| `fasthep-workshop` | Tutorials, examples, and training material | --- | [FAST-HEP/fasthep-workshop](https://github.com/FAST-HEP/fasthep-workshop) |
| `fasthep` | Meta package and compatibility bundle | --- | [FAST-HEP/fasthep](https://github.com/FAST-HEP/fasthep) |
| `fasthep-dev` | Integration workspace and ecosystem validation | --- | [FAST-HEP/fasthep-dev](https://github.com/FAST-HEP/fasthep-dev) |
