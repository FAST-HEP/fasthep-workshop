from pathlib import Path


def test_template_author_exists() -> None:
    assert Path("author.yaml").exists()
