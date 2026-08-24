# Provenance Seed Policy

This directory records provenance decisions for the Sacrificial Debt manual
pilot before any raw source text is ingested.

The first seed records in `projects/sacrificial-debt/data/sources.jsonl` are
metadata-only records. They identify bounded source leads selected by the
manual pilot corpus manifest, but they do not copy source text, scans, PDFs, or
critical apparatus into the public repository.

## Checksum Scope

Source records use `checksum_scope` to state what `checksum_sha256` identifies:

- `local_file`: a local source file committed or stored under the approved raw
  source policy;
- `remote_file`: a remote source file captured by checksum without committing
  the file;
- `metadata_record`: the normalized source metadata record, excluding the
  `checksum_sha256` field itself.

For issue #3, all seed records use `metadata_record`. This preserves an
auditable checksum while avoiding unauthorized redistribution of copyrighted or
rights-uncertain source text.

## Remote Sources and Local Working Copies

Remote sources may still be copied into a local, gitignored working corpus for
analysis. When that happens, keep both identities visible:

- `canonical_url`: the page or file URL used for acquisition;
- `source_location_name`: a human-readable name for the collection, portal,
  catalog, database, archive location, or source surface where the artifact was
  found;
- `accessed_at`: the exact datetime the page/file was accessed, scraped, or
  downloaded;
- `capture_method`: `downloaded_file` for a downloaded file,
  `static_html_scrape` for text captured from the URL response before
  JavaScript execution, `browser_rendered_capture` for text captured after a
  browser rendered JavaScript-dependent page, `ocr_text` for machine text
  extracted from an image or scan, `manual_transcription` for human-entered text
  copied from a viewed source, or `manual_metadata_review` when only
  bibliographic metadata was recorded;
- `local_path`: the gitignored local working copy when one exists;
- `checksum_scope`: `local_file` when hashing the local copy, `remote_file`
  when hashing a remote artifact without storing it locally, or
  `metadata_record` when no source content has been captured.

Do not gitignore source captures merely because they were scraped, downloaded,
OCRed, or manually transcribed. Gitignore them only when rights,
redistribution, privacy, sensitivity, or repository-size constraints require
keeping the artifact out of public GitHub.

For public-domain, openly licensed, or otherwise redistributable material,
committing the captured text or file is permitted when the source record
documents the URL, access datetime, capture method, local path, checksum, and
redistribution basis.

For copyrighted, restricted, rights-uncertain, or non-redistributable material,
prefer local gitignored working copies plus source records over committing
source text to the public repository. Every gitignored source must also appear
in `GITIGNORED_SOURCES.md` with enough reacquisition instructions for another
authorized researcher to obtain the same document.

Use `source_location_name` for human navigation and citation context, not as a
replacement for `canonical_url`. For example, a source may have
`repository: University of Michigan` and
`source_location_name: University of Michigan Lincoln Project`.

Use `browser_rendered_capture` when the loaded HTML does not contain the source
text and the usable text appears only after JavaScript execution. Record the URL
and `accessed_at` datetime for the rendered capture, and hash the saved local
rendered text or capture artifact with `checksum_scope: local_file`.

Use `ocr_text` when local working text is produced by OCR from a scan, page
image, or PDF image layer. Preserve the scan/file source record separately when
possible, and record OCR engine/settings in provenance notes until a dedicated
capture-event schema exists.

Use `manual_transcription` when a human types or corrects source text from an
image, scan, physical source, or non-copyable interface. Mark the transcription
as a local working artifact, hash it, and keep later segment/proposition records
tied to the source coordinates that were transcribed.

## Translation and Original-Language Text

Source records must distinguish original-language artifacts from translations:

- `language`: the language of the captured or described artifact;
- `original_language`: the language of the original source when the artifact is
  translated;
- `translation_status`: `original_language`, `human_translation`,
  `machine_translation`, `mixed_translation`, `not_applicable`, or `unknown`;
- `translator`: the named translator, editor-translator, model, or responsible
  translation agent when known;
- `translation_source_id`: the source record for the original-language artifact
  when a translation is registered separately;
- `translation_notes`: uncertainty, edition relationship, translation basis, or
  review status.

High-value translated evidence must preserve original-language text whenever
rights permit. If the original-language artifact cannot be committed, register
the local gitignored original in `GITIGNORED_SOURCES.md` and link translated
working text back to it with `translation_source_id` or provenance notes.

For issue #3, seed records are source-level provenance records only. Exact
alignment between original text, translation, segment coordinates, and
proposition text belongs in later document/segment/proposition records.

## Tier and Rights Rule

Every seed source records an initial `corpus_tier`, copyright status,
redistribution status, reliability assessment, and provenance note.

Tier 3 sources are leads, not coded evidence. Tier 1 source records still require
document, segment, proposition, and annotation records before they can support
interpretive claims.
