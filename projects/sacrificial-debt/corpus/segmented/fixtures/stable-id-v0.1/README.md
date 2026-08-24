# Stable ID Fixture v0.1

This fixture contains one synthetic source, one synthetic document, two
paragraph segments, and one proposition.

It exists only to validate stable identifier behavior and coordinate checks:

- source to document referential integrity;
- document to segment referential integrity;
- proposition to segment referential integrity;
- segment `text_hash` values;
- required character coordinate bounds in fixture records;
- explicit `coordinate_scope: segment_text` semantics.

The text is synthetic and is not historical evidence.
