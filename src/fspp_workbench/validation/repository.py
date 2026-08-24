from dataclasses import dataclass, field
from pathlib import Path

from pydantic import ValidationError

from fspp_workbench.core.hashing import sha256_text
from fspp_workbench.core.jsonl import read_jsonl
from fspp_workbench.core.models import Document, Proposition, Segment, Source


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _validate_file(path: Path, model: type, report: ValidationReport) -> list[dict]:
    records = []
    if not path.exists():
        report.warnings.append(f"Missing optional scaffold data file: {path}")
        return records
    for line_no, record in enumerate(read_jsonl(path), 1):
        try:
            model.model_validate(record)
            records.append(record)
        except ValidationError as exc:
            report.errors.append(f"{path}:{line_no}: {exc}")
    return records


def _validate_coordinate_bounds(
    *,
    record_type: str,
    record_id: str,
    char_start: int | None,
    char_end: int | None,
    text: str,
    report: ValidationReport,
) -> None:
    if (char_start is None) != (char_end is None):
        report.errors.append(
            f"{record_type} {record_id} must provide both char_start and char_end "
            "or neither"
        )
        return
    if char_start is None or char_end is None:
        return
    if char_start > char_end:
        report.errors.append(f"{record_type} {record_id} has char_start after char_end")
    if char_end > len(text):
        report.errors.append(f"{record_type} {record_id} char_end exceeds text length")


def _validate_record_set(
    *,
    label: str,
    sources: list[dict],
    docs: list[dict],
    segments: list[dict],
    props: list[dict],
    report: ValidationReport,
) -> None:
    source_ids = {x["source_id"] for x in sources}
    doc_ids = {x["document_id"] for x in docs}
    segment_by_id = {x["segment_id"]: x for x in segments}
    segment_ids = set(segment_by_id)

    for record in docs:
        if record["source_id"] not in source_ids:
            report.errors.append(
                f"{label}: Document {record['document_id']} references missing source "
                f"{record['source_id']}"
            )
    for record in segments:
        if record["document_id"] not in doc_ids:
            report.errors.append(
                f"{label}: Segment {record['segment_id']} references missing document "
                f"{record['document_id']}"
            )
        if record["text_hash"] != sha256_text(record["text"]):
            report.errors.append(f"{label}: Segment {record['segment_id']} text_hash mismatch")
        _validate_coordinate_bounds(
            record_type=f"{label}: Segment",
            record_id=record["segment_id"],
            char_start=record.get("char_start"),
            char_end=record.get("char_end"),
            text=record["text"],
            report=report,
        )
    for record in props:
        if record["document_id"] not in doc_ids:
            report.errors.append(
                f"{label}: Proposition {record['proposition_id']} references missing document "
                f"{record['document_id']}"
            )
        missing = set(record["segment_ids"]) - segment_ids
        if missing:
            report.errors.append(
                f"{label}: Proposition {record['proposition_id']} references missing "
                f"segments {sorted(missing)}"
            )
            continue
        segment_text = "\n".join(segment_by_id[x]["text"] for x in record["segment_ids"])
        if record["exact_text"] not in segment_text:
            report.errors.append(
                f"{label}: Proposition {record['proposition_id']} exact_text is not "
                "present in its referenced segment text"
            )
        _validate_coordinate_bounds(
            record_type=f"{label}: Proposition",
            record_id=record["proposition_id"],
            char_start=record.get("char_start"),
            char_end=record.get("char_end"),
            text=record["exact_text"],
            report=report,
        )


def validate_project(root: Path) -> ValidationReport:
    report = ValidationReport()
    data = root / "projects" / "sacrificial-debt" / "data"
    sources = _validate_file(data / "sources.jsonl", Source, report)
    docs = _validate_file(data / "documents.jsonl", Document, report)
    segments = _validate_file(data / "segments.jsonl", Segment, report)
    props = _validate_file(data / "propositions.jsonl", Proposition, report)

    _validate_record_set(
        label="canonical data",
        sources=sources,
        docs=docs,
        segments=segments,
        props=props,
        report=report,
    )

    fixture_root = (
        root
        / "projects"
        / "sacrificial-debt"
        / "corpus"
        / "segmented"
        / "fixtures"
    )
    for fixture_dir in sorted(path for path in fixture_root.glob("*") if path.is_dir()):
        fixture_sources = _validate_file(fixture_dir / "sources.jsonl", Source, report)
        fixture_docs = _validate_file(fixture_dir / "documents.jsonl", Document, report)
        fixture_segments = _validate_file(fixture_dir / "segments.jsonl", Segment, report)
        fixture_props = _validate_file(fixture_dir / "propositions.jsonl", Proposition, report)
        _validate_record_set(
            label=f"segmentation fixture {fixture_dir.name}",
            sources=fixture_sources,
            docs=fixture_docs,
            segments=fixture_segments,
            props=fixture_props,
            report=report,
        )
    return report
