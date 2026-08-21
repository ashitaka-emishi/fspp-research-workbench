import platform
from pathlib import Path

import typer

from fspp_workbench.schema import render_schemas
from fspp_workbench.validation.repository import validate_project

app = typer.Typer(help="FSPP Research Workbench research-engineering CLI")
schema_app = typer.Typer(help="JSON Schema commands")
app.add_typer(schema_app, name="schema")


def repo_root() -> Path:
    here = Path.cwd()
    for candidate in [here, *here.parents]:
        if (candidate / "pyproject.toml").exists() and (candidate / "projects").exists():
            return candidate
    raise typer.BadParameter("Run from inside the FSPP Research Workbench repository")


@app.command()
def doctor() -> None:
    """Check basic local development prerequisites."""
    typer.echo(f"Python: {platform.python_version()}")
    typer.echo(f"Repository: {repo_root()}")
    typer.echo("Core Python environment: OK")
    typer.echo("Quarto is optional until publication rendering.")


@app.command()
def validate() -> None:
    """Validate canonical scaffold data and referential integrity."""
    report = validate_project(repo_root())
    for warning in report.warnings:
        typer.echo(f"WARNING: {warning}")
    for error in report.errors:
        typer.echo(f"ERROR: {error}")
    if not report.ok:
        raise typer.Exit(code=1)
    typer.echo("Validation passed.")


@schema_app.command("build")
def schema_build() -> None:
    target = repo_root() / "schemas"
    rendered = render_schemas(target)
    typer.echo(f"Wrote {len(rendered)} schemas to {target}")


@schema_app.command("check")
def schema_check() -> None:
    root = repo_root()
    target = root / "schemas"
    current = {p.name: p.read_text(encoding="utf-8") for p in target.glob("*.schema.json")}
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        rendered = render_schemas(Path(tmp))
    expected = {f"{name}.schema.json": text for name, text in rendered.items()}
    if current != expected:
        typer.echo("Checked-in JSON Schemas are stale. Run: fspp schema build")
        raise typer.Exit(code=1)
    typer.echo("Checked-in JSON Schemas are current.")

if __name__ == "__main__":
    app()
