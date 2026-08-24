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

Use `master` as the default branch in GitHub repository settings.

## Repository Settings

Recommended setup after the first push:

- Repository description: `Reusable research environment for FSPP political pathology projects.`
- Website: `https://ashitaka-emishi.github.io/fspp-research-wrokbench/`
- Issues: enabled.
- Actions: enabled.
- Pages source: GitHub Actions.
- Default branch: `master`.

Keep branch protection on `master` aligned with the SDLC workflow:

- Require pull requests before merging.
- Require status checks when GitHub Actions are available.
- Use squash merge for normal PR closeout.
- Allow repository-owner self-approval only if that is the current maintainer
  policy.

## Issues And Milestones

Use the Markdown issue templates under `.github/ISSUE_TEMPLATE/`; they carry the
versioned `fspp-issue-contract` marker validated by the SDLC helper. Avoid
creating tracked SDLC issues from ad hoc GitHub forms, because they will bypass
the required contract sections.

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
