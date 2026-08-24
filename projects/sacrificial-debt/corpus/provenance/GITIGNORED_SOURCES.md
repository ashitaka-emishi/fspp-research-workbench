# Gitignored Source Reacquisition Log

This log records local working sources that are intentionally not committed to
the public repository. A source belongs here only when the local artifact is
gitignored because of copyright, redistribution limits, privacy, sensitivity, or
repository-size constraints.

Do not add entries for redistributable captures that are committed to Git.

Every entry must correspond to a source record in
`projects/sacrificial-debt/data/sources.jsonl`.

| Source ID | Local path | Reason gitignored | Where/how to reacquire | Accessed at | Checksum scope | SHA-256 |
|---|---|---|---|---|---|---|
| _No gitignored source artifacts registered yet._ |  |  |  |  |  |  |

## Entry Rules

- `Source ID` must match `sources.jsonl`.
- `Local path` should point to the gitignored working copy used locally.
- `Reason gitignored` should distinguish copyright, rights uncertainty,
  contractual restriction, privacy/sensitivity, or repository-size constraint.
- `Where/how to reacquire` should include the stable URL, archive/catalog
  instructions, edition details, access requirements, or purchase/library route.
- `Accessed at` should match the source record's `accessed_at` value when the
  local artifact was captured from a remote source.
- `Checksum scope` should usually be `local_file` for the gitignored working
  copy.
- `SHA-256` should match the source record when that record identifies the local
  gitignored artifact.
