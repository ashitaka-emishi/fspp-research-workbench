# Segmentation Fixtures

Segmentation fixtures prove that stable identifiers, source/document/segment
relationships, text hashes, and character-coordinate checks work before the
manual pilot ingests rights-reviewed source text.

Fixtures may contain synthetic text only unless a later rights review explicitly
permits redistribution of a real source excerpt. Synthetic fixture records must
remain clearly labeled as fixtures and must not be used as evidence for
research claims.

Each fixture set should include:

- `sources.jsonl`
- `documents.jsonl`
- `segments.jsonl`
- `propositions.jsonl`

`uv run fspp validate` checks both canonical project data and these fixture
sets.
