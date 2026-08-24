# Stable ID Fixture v0.1

This fixture contains one synthetic source, one synthetic document, two
paragraph segments, one full page text capture, and one proposition.

It exists only to validate stable identifier behavior and coordinate checks:

- source to document referential integrity;
- document to segment referential integrity;
- proposition to segment referential integrity;
- full text capture hashing and source/document linkage;
- segment `text_hash` values;
- required character coordinate bounds in fixture records;
- explicit `coordinate_scope: segment_text` semantics;
- page-relative coordinate validation through `coordinate_scope: page_text`.

The text is synthetic and is not historical evidence.
