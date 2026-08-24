from pathlib import Path

from fspp_workbench.core.hashing import sha256_text
from fspp_workbench.core.ids import validate_id
from fspp_workbench.core.jsonl import read_jsonl
from fspp_workbench.core.models import Document, FullTextCapture, Proposition, Segment, Source
from fspp_workbench.validation.repository import (
    ValidationReport,
    _validate_record_set,
    validate_project,
)

FIXTURE_ROOT = Path(
    "projects/sacrificial-debt/corpus/segmented/fixtures/stable-id-v0.1"
)


def test_stable_id_fixture_records_validate() -> None:
    sources = [
        Source.model_validate(record)
        for record in read_jsonl(FIXTURE_ROOT / "sources.jsonl")
    ]
    docs = [
        Document.model_validate(record)
        for record in read_jsonl(FIXTURE_ROOT / "documents.jsonl")
    ]
    segments = [
        Segment.model_validate(record)
        for record in read_jsonl(FIXTURE_ROOT / "segments.jsonl")
    ]
    full_text_captures = [
        FullTextCapture.model_validate(record)
        for record in read_jsonl(FIXTURE_ROOT / "full-text-captures.jsonl")
    ]
    props = [
        Proposition.model_validate(record)
        for record in read_jsonl(FIXTURE_ROOT / "propositions.jsonl")
    ]

    assert len(sources) == 1
    assert len(docs) == 1
    assert len(full_text_captures) == 1
    assert len(segments) == 2
    assert len(props) == 1

    for record_id in [
        docs[0].document_id,
        *(segment.segment_id for segment in segments),
        props[0].proposition_id,
    ]:
        assert validate_id(record_id) == record_id

    source_ids = {source.source_id for source in sources}
    doc_ids = {doc.document_id for doc in docs}
    segment_ids = {segment.segment_id for segment in segments}

    assert docs[0].source_id in source_ids
    assert all(segment.document_id in doc_ids for segment in segments)
    assert props[0].document_id in doc_ids
    assert set(props[0].segment_ids) <= segment_ids


def test_stable_id_fixture_hashes_and_coordinates_are_exact() -> None:
    full_text_captures = [
        FullTextCapture.model_validate(record)
        for record in read_jsonl(FIXTURE_ROOT / "full-text-captures.jsonl")
    ]
    segments = [
        Segment.model_validate(record)
        for record in read_jsonl(FIXTURE_ROOT / "segments.jsonl")
    ]
    props = [
        Proposition.model_validate(record)
        for record in read_jsonl(FIXTURE_ROOT / "propositions.jsonl")
    ]

    capture = full_text_captures[0]
    assert capture.coordinate_scope == "page_text"
    assert capture.page_label == "fixture-1"
    assert capture.text_hash == sha256_text(capture.text)

    first_segment = segments[0]
    assert first_segment.coordinate_scope == "page_text"
    assert first_segment.text_hash == sha256_text(first_segment.text)
    assert first_segment.char_start == 72
    assert first_segment.char_end == 134
    assert capture.text[first_segment.char_start : first_segment.char_end] == first_segment.text

    second_segment = segments[1]
    assert second_segment.coordinate_scope == "segment_text"
    assert second_segment.text_hash == sha256_text(second_segment.text)
    assert second_segment.char_start == 0
    assert second_segment.char_end == len(second_segment.text)

    segment_text_by_id = {segment.segment_id: segment.text for segment in segments}
    for prop in props:
        assert prop.coordinate_scope == "page_text"
        assert prop.char_start == 72
        assert prop.char_end == 134
        assert capture.text[prop.char_start : prop.char_end] == prop.exact_text
        assert prop.exact_text in "\n".join(
            segment_text_by_id[segment_id] for segment_id in prop.segment_ids
        )


def test_page_text_coordinates_require_a_matching_full_text_capture() -> None:
    sources = list(read_jsonl(FIXTURE_ROOT / "sources.jsonl"))
    docs = list(read_jsonl(FIXTURE_ROOT / "documents.jsonl"))
    segments = list(read_jsonl(FIXTURE_ROOT / "segments.jsonl"))
    props = list(read_jsonl(FIXTURE_ROOT / "propositions.jsonl"))
    report = ValidationReport()

    _validate_record_set(
        label="fixture without capture",
        sources=sources,
        docs=docs,
        full_text_captures=[],
        segments=segments,
        props=props,
        report=report,
    )

    assert not report.ok
    assert any("has no matching page_text full text capture" in error for error in report.errors)


def test_repository_validation_includes_segmentation_fixtures() -> None:
    report = validate_project(Path("."))

    assert report.ok, report.errors
