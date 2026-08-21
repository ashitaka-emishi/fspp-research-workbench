from pathlib import Path


def test_shared_infrastructure_does_not_import_project_theory() -> None:
    root = Path(__file__).parents[1] / "src" / "fspp_workbench"
    violations = []
    for path in root.rglob("*.py"):
        if "projects" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if "fspp_workbench.projects" in text and path.name != "schema.py":
            violations.append(str(path))
    assert not violations, f"Shared modules import project theory: {violations}"
