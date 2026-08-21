.PHONY: setup test lint validate schemas doctor site clean

setup:
	uv venv .venv --python 3.14
	uv sync --all-extras

doctor:
	uv run fspp doctor

schemas:
	uv run fspp schema build

validate:
	uv run fspp validate

test:
	uv run pytest

lint:
	uv run ruff check .

site:
	cd publication && quarto render
	cd publication/engineering && quarto render
	cd publication/projects/sacrificial-debt && quarto render

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache publication/_site
