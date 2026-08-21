from pathlib import Path

from fspp_workbench.schema import render_schemas


def test_schema_generation(tmp_path: Path) -> None:
    rendered = render_schemas(tmp_path)
    assert "source" in rendered
    assert (tmp_path / "sd-annotation.schema.json").exists()
