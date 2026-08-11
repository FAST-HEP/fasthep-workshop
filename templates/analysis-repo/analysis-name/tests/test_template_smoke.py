from pathlib import Path


def test_template_workflow_exists() -> None:
    assert Path("workflow.yaml").exists()
