# Start This as a New GitHub Project

After extracting the scaffold:

```bash
cd fspp-research-workbench
git init
git add .
git commit -m "Initialize FSPP Research Workbench"
git branch -M master
```

Create an empty GitHub repository, then:

```bash
git remote add origin git@github.com:ashitaka-emishi/fspp-research-wrokbench.git
git push -u origin master
```

Then open in VS Code:

```bash
code .
```

Bootstrap:

```bash
uv venv .venv --python 3.14
uv sync --all-extras
uv run fspp doctor
uv run fspp schema check
uv run fspp validate
uv run pytest
```

Read `CODEX_START_HERE.md` before assigning the first Codex task.
