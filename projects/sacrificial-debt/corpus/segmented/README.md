# Segmented Corpus

This directory holds segmented corpus artifacts for the Sacrificial Debt
manual pilot.

Stable document, segment, and proposition identifiers are permanent once they
enter a reviewed or released dataset. If a document is resegmented, split,
merged, corrected, or re-coordinated, preserve the old record and use lineage
metadata to supersede it with a new identifier. Do not renumber records because
ordering changed.

Use `coordinate_scope` to state what `char_start` and `char_end` are relative
to:

- `segment_text`: coordinates are relative to the stored segment text;
- `page_text`: coordinates are relative to a full captured page text;
- `document_text`: coordinates are relative to a full captured document text;
- `source_text`: coordinates are relative to a complete source-level capture.

When only a short excerpt is committed, use `segment_text` and say so in the
lineage note. Do not imply page- or document-relative coordinates until the
corresponding full text is captured, reviewed, and hashable.

Full page, document, and source text captures are recorded in
`projects/sacrificial-debt/data/full-text-captures.jsonl` for canonical project
data and in each fixture directory's `full-text-captures.jsonl` for synthetic
validation records. A full-text capture stores the captured text, hash, source
or document relationship, capture method, capture time, rights/redistribution
status, and lineage. Segment and proposition coordinates with `page_text`,
`document_text`, or `source_text` scope must slice-match a corresponding
full-text capture.

Use `locator_note` for human-readable location help, such as section heading,
item number, page label, table number, paragraph label, or archival folio
description. A locator note helps reviewers find the excerpt, but it does not
replace exact machine-checkable coordinates when those coordinates exist.

Reviewed records may remain `segment_text` scoped when a full capture is not
yet rights-reviewed for public Git. Upgrade to page-, document-, or
source-relative coordinates only by preserving lineage and validating against a
hashable capture.

The `fixtures/` subdirectory contains synthetic validation records. Fixture
text is not historical evidence, is not part of the pilot corpus, and must not
be coded as a Sacrificial Debt source claim.
