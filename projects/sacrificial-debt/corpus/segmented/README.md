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

Use `locator_note` for human-readable location help, such as section heading,
item number, page label, table number, paragraph label, or archival folio
description. A locator note helps reviewers find the excerpt, but it does not
replace exact machine-checkable coordinates when those coordinates exist.

The `fixtures/` subdirectory contains synthetic validation records. Fixture
text is not historical evidence, is not part of the pilot corpus, and must not
be coded as a Sacrificial Debt source claim.
