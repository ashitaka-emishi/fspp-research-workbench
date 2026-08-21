#!/usr/bin/env bash
set -euo pipefail
uv venv .venv --python 3.14
uv sync --all-extras
uv run fspp schema build
uv run fspp validate
uv run pytest
