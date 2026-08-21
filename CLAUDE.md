# FSPP Research Workbench — Claude Backup Instructions

Codex is the primary AI coding agent for this repository. When Claude AI is
used as a backup agent, follow `AGENTS.md` first.

## SDLC Workflow

When the user types `sdlc`, `sldc`, or `$sdlc-workflow` — with or without a
following issue number, issue range, or `next` — read and follow
`.agents/skills/sdlc-workflow/SKILL.md` in full before taking action.

Use the repository defaults in that skill:

- GitHub repo: `ashitaka-emishi/fspp-research-wrokbench`
- Default branch: `master`
- Python namespace: `fspp_workbench`
- CLI: `fspp`

Claude-authored commits use:

```text
Co-authored-by: Claude <noreply@anthropic.com>
```

Do not merge, close issues, approve research artifacts, promote claims, publish
releases, or alter codebook semantics unless the user explicitly authorizes that
workflow.
