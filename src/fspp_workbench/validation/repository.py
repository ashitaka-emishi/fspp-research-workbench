from dataclasses import dataclass, field
from pathlib import Path

from pydantic import ValidationError

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


def validate_project(root: Path) -> ValidationReport:
    report = ValidationReport()
    data = root / "projects" / "sacrificial-debt" / "data"
    sources = _validate_file(data / "sources.jsonl", Source, report)
    docs = _validate_file(data / "documents.jsonl", Document, report)
    segments = _validate_file(data / "segments.jsonl", Segment, report)
    props = _validate_file(data / "propositions.jsonl", Proposition, report)

    source_ids = {x["source_id"] for x in sources}
    doc_ids = {x["document_id"] for x in docs}
    segment_ids = {x["segment_id"] for x in segments}

    for record in docs:
        if record["source_id"] not in source_ids:
            report.errors.append(
                f"Document {record['document_id']} references missing source {record['source_id']}"
            )
    for record in segments:
        if record["document_id"] not in doc_ids:
            report.errors.append(
                f"Segment {record['segment_id']} references missing document "
                f"{record['document_id']}"
            )
    for record in props:
        if record["document_id"] not in doc_ids:
            report.errors.append(
                f"Proposition {record['proposition_id']} references missing document "
                f"{record['document_id']}"
            )
        missing = set(record["segment_ids"]) - segment_ids
        if missing:
            report.errors.append(
                f"Proposition {record['proposition_id']} references missing segments "
                f"{sorted(missing)}"
            )
    return report
