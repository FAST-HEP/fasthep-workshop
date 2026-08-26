from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "_ext"))

project = "FAST-HEP Workshop"
author = "FAST-HEP contributors"

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxcontrib.mermaid",
    "sphinx.ext.mathjax",
    "mermaid_styles",

]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

html_theme = "pydata_sphinx_theme"

html_static_path = ["_static"]

html_theme_options = {
    "github_url": "https://github.com/FAST-HEP/fasthep-workshop",
    "logo": {
        "text": "FAST-HEP Workshop",
    },
    "navbar_align": "left",
}

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "substitution",
]

mermaid_params = [
    "--theme",
    "forest",
    "--backgroundColor",
    "transparent",
]
mermaid_height = "auto"


def sync_tutorial_expected_assets() -> None:
    docs_dir = Path(__file__).parent.resolve()
    repo_root = docs_dir.parent.resolve()

    tutorials_dir = repo_root / "tutorials"
    static_root = docs_dir / "_static" / "_generated" / "tutorials"

    if static_root.exists():
        shutil.rmtree(static_root)
    static_root.mkdir(parents=True, exist_ok=True)

    for expected_dir in tutorials_dir.glob("**/expected"):
        tutorial_dir = expected_dir.parent
        rel_tutorial = tutorial_dir.relative_to(tutorials_dir)

        for subdir in ("plots", "tables", "snippets"):
            src = expected_dir / subdir
            if not src.exists():
                continue

            dst = static_root / rel_tutorial / subdir
            shutil.copytree(src, dst, dirs_exist_ok=True)


sync_tutorial_expected_assets()

exclude_patterns = [
    "_build",
    "archive/**",
]
mermaid_init_config = {
    "startOnLoad": True,
    "theme": "base",
    "themeVariables": {
        "background": "#ffffff",
        "primaryTextColor": "#111111",
        "lineColor": "#5f6368",
        "fontSize": "18px",
    },
    "flowchart": {
        "htmlLabels": True,
        "nodeSpacing": 40,
        "rankSpacing": 50,
        "curve": "basis",
    },
}
