from dataclasses import dataclass, field
from pathlib import Path

from pydantic import ValidationError

from fspp_workbench.core.hashing import sha256_text
from fspp_workbench.core.jsonl import read_jsonl
from fspp_workbench.core.models import Document, FullTextCapture, Proposition, Segment, Source
from fspp_workbench.schema import MODELS

Annotation = MODELS["sd-annotation"]
NegativeEvidence = MODELS["sd-negative-evidence"]
RivalExplanation = MODELS["sd-rival-explanation"]


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
    text: str | None,
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
    if text is not None and char_end > len(text):
        report.errors.append(f"{record_type} {record_id} char_end exceeds text length")


def _capture_text_for_segment(
    *,
    segment: dict,
    document_by_id: dict[str, dict],
    page_capture_by_key: dict[tuple[str, str], dict],
    document_capture_by_id: dict[str, dict],
    source_capture_by_id: dict[str, dict],
    label: str,
    report: ValidationReport,
) -> str | None:
    coordinate_scope = segment.get("coordinate_scope", "segment_text")
    if coordinate_scope == "segment_text":
        return segment["text"]

    document = document_by_id.get(segment["document_id"])
    if document is None:
        return None

    if coordinate_scope == "page_text":
        page_label = segment.get("page_label")
        if not page_label:
            report.errors.append(
                f"{label}: Segment {segment['segment_id']} uses page_text coordinates "
                "without page_label"
            )
            return None
        capture = page_capture_by_key.get((segment["document_id"], page_label))
    elif coordinate_scope == "document_text":
        capture = document_capture_by_id.get(segment["document_id"])
    elif coordinate_scope == "source_text":
        capture = source_capture_by_id.get(document["source_id"])
    else:
        capture = None

    if capture is None:
        report.errors.append(
            f"{label}: Segment {segment['segment_id']} has no matching "
            f"{coordinate_scope} full text capture"
        )
        return None
    return capture["text"]


def _capture_text_for_proposition(
    *,
    proposition: dict,
    segment_by_id: dict[str, dict],
    document_by_id: dict[str, dict],
    page_capture_by_key: dict[tuple[str, str], dict],
    document_capture_by_id: dict[str, dict],
    source_capture_by_id: dict[str, dict],
    label: str,
    report: ValidationReport,
) -> str | None:
    coordinate_scope = proposition.get("coordinate_scope", "segment_text")
    if coordinate_scope == "segment_text":
        return "\n".join(segment_by_id[x]["text"] for x in proposition["segment_ids"])

    document = document_by_id.get(proposition["document_id"])
    if document is None:
        return None

    if coordinate_scope == "page_text":
        page_labels = {
            segment_by_id[segment_id].get("page_label")
            for segment_id in proposition["segment_ids"]
        }
        page_labels.discard(None)
        if len(page_labels) != 1:
            report.errors.append(
                f"{label}: Proposition {proposition['proposition_id']} uses page_text "
                "coordinates but referenced segments do not resolve to one page_label"
            )
            return None
        capture = page_capture_by_key.get((proposition["document_id"], next(iter(page_labels))))
    elif coordinate_scope == "document_text":
        capture = document_capture_by_id.get(proposition["document_id"])
    elif coordinate_scope == "source_text":
        capture = source_capture_by_id.get(document["source_id"])
    else:
        capture = None

    if capture is None:
        report.errors.append(
            f"{label}: Proposition {proposition['proposition_id']} has no matching "
            f"{coordinate_scope} full text capture"
        )
        return None
    return capture["text"]


def _validate_record_set(
    *,
    label: str,
    sources: list[dict],
    docs: list[dict],
    full_text_captures: list[dict] | None,
    segments: list[dict],
    props: list[dict],
    annotations: list[dict] | None = None,
    negative_evidence: list[dict] | None = None,
    rival_explanations: list[dict] | None = None,
    report: ValidationReport,
) -> None:
    annotations = annotations or []
    negative_evidence = negative_evidence or []
    rival_explanations = rival_explanations or []
    source_ids = {x["source_id"] for x in sources}
    document_by_id = {x["document_id"]: x for x in docs}
    doc_ids = set(document_by_id)
    page_capture_by_key: dict[tuple[str, str], dict] = {}
    document_capture_by_id: dict[str, dict] = {}
    source_capture_by_id: dict[str, dict] = {}
    segment_by_id = {x["segment_id"]: x for x in segments}
    segment_ids = set(segment_by_id)
    proposition_ids = {x["proposition_id"] for x in props}

    for record in docs:
        if record["source_id"] not in source_ids:
            report.errors.append(
                f"{label}: Document {record['document_id']} references missing source "
                f"{record['source_id']}"
            )
    for record in full_text_captures or []:
        if record["source_id"] not in source_ids:
            report.errors.append(
                f"{label}: Full text capture {record['full_text_capture_id']} references "
                f"missing source {record['source_id']}"
            )
        document_id = record.get("document_id")
        if document_id is not None:
            document = document_by_id.get(document_id)
            if document is None:
                report.errors.append(
                    f"{label}: Full text capture {record['full_text_capture_id']} "
                    f"references missing document {document_id}"
                )
            elif document["source_id"] != record["source_id"]:
                report.errors.append(
                    f"{label}: Full text capture {record['full_text_capture_id']} source "
                    "does not match its document source"
                )
        if record["text_hash"] != sha256_text(record["text"]):
            report.errors.append(
                f"{label}: Full text capture {record['full_text_capture_id']} text_hash mismatch"
            )
        coordinate_scope = record["coordinate_scope"]
        if coordinate_scope == "page_text":
            if document_id is None or not record.get("page_label"):
                report.errors.append(
                    f"{label}: Full text capture {record['full_text_capture_id']} "
                    "with page_text scope requires document_id and page_label"
                )
            else:
                key = (document_id, record["page_label"])
                if key in page_capture_by_key:
                    report.errors.append(
                        f"{label}: Duplicate page_text full text capture for "
                        f"document {document_id} page {record['page_label']}"
                    )
                page_capture_by_key[key] = record
        elif coordinate_scope == "document_text":
            if document_id is None:
                report.errors.append(
                    f"{label}: Full text capture {record['full_text_capture_id']} "
                    "with document_text scope requires document_id"
                )
            else:
                if document_id in document_capture_by_id:
                    report.errors.append(
                        f"{label}: Duplicate document_text full text capture for "
                        f"document {document_id}"
                    )
                document_capture_by_id[document_id] = record
        elif coordinate_scope == "source_text":
            if record["source_id"] in source_capture_by_id:
                report.errors.append(
                    f"{label}: Duplicate source_text full text capture for source "
                    f"{record['source_id']}"
                )
            source_capture_by_id[record["source_id"]] = record
    for record in segments:
        if record["document_id"] not in doc_ids:
            report.errors.append(
                f"{label}: Segment {record['segment_id']} references missing document "
                f"{record['document_id']}"
            )
        if record["text_hash"] != sha256_text(record["text"]):
            report.errors.append(f"{label}: Segment {record['segment_id']} text_hash mismatch")
        coordinate_text = _capture_text_for_segment(
            segment=record,
            document_by_id=document_by_id,
            page_capture_by_key=page_capture_by_key,
            document_capture_by_id=document_capture_by_id,
            source_capture_by_id=source_capture_by_id,
            label=label,
            report=report,
        )
        _validate_coordinate_bounds(
            record_type=f"{label}: Segment",
            record_id=record["segment_id"],
            char_start=record.get("char_start"),
            char_end=record.get("char_end"),
            text=coordinate_text,
            report=report,
        )
        if (
            coordinate_text is not None
            and record.get("char_start") is not None
            and record.get("char_end") is not None
            and coordinate_text[record["char_start"] : record["char_end"]] != record["text"]
        ):
            report.errors.append(
                f"{label}: Segment {record['segment_id']} coordinate slice "
                "does not match text"
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
        coordinate_text = _capture_text_for_proposition(
            proposition=record,
            segment_by_id=segment_by_id,
            document_by_id=document_by_id,
            page_capture_by_key=page_capture_by_key,
            document_capture_by_id=document_capture_by_id,
            source_capture_by_id=source_capture_by_id,
            label=label,
            report=report,
        )
        _validate_coordinate_bounds(
            record_type=f"{label}: Proposition",
            record_id=record["proposition_id"],
            char_start=record.get("char_start"),
            char_end=record.get("char_end"),
            text=coordinate_text,
            report=report,
        )
        if (
            coordinate_text is not None
            and record.get("char_start") is not None
            and record.get("char_end") is not None
            and coordinate_text[record["char_start"] : record["char_end"]]
            != record["exact_text"]
        ):
            report.errors.append(
                f"{label}: Proposition {record['proposition_id']} coordinate slice "
                "does not match exact_text"
            )
    for record in annotations:
        if record["proposition_id"] not in proposition_ids:
            report.errors.append(
                f"{label}: Annotation {record['annotation_id']} references missing "
                f"proposition {record['proposition_id']}"
            )
    for record in negative_evidence:
        missing = set(record["proposition_ids"]) - proposition_ids
        if missing:
            report.errors.append(
                f"{label}: Negative evidence {record['negative_evidence_id']} "
                f"references missing propositions {sorted(missing)}"
            )
    for record in rival_explanations:
        proposition_id = record.get("proposition_id")
        if proposition_id is not None and proposition_id not in proposition_ids:
            report.errors.append(
                f"{label}: Rival explanation {record['rival_explanation_id']} "
                f"references missing proposition {proposition_id}"
            )
        missing = {
            evidence_ref
            for evidence_ref in record["evidence_refs"]
            if evidence_ref.startswith("sd-prop-") and evidence_ref not in proposition_ids
        }
        if missing:
            report.errors.append(
                f"{label}: Rival explanation {record['rival_explanation_id']} "
                f"references missing evidence refs {sorted(missing)}"
            )


def validate_project(root: Path) -> ValidationReport:
    report = ValidationReport()
    data = root / "projects" / "sacrificial-debt" / "data"
    sources = _validate_file(data / "sources.jsonl", Source, report)
    docs = _validate_file(data / "documents.jsonl", Document, report)
    full_text_captures = _validate_file(
        data / "full-text-captures.jsonl", FullTextCapture, report
    )
    segments = _validate_file(data / "segments.jsonl", Segment, report)
    props = _validate_file(data / "propositions.jsonl", Proposition, report)
    annotations = _validate_file(data / "annotations" / "reference.jsonl", Annotation, report)
    negative_evidence = _validate_file(data / "negative-evidence.jsonl", NegativeEvidence, report)
    rival_explanations = _validate_file(
        data / "rival-explanations.jsonl", RivalExplanation, report
    )

    _validate_record_set(
        label="canonical data",
        sources=sources,
        docs=docs,
        full_text_captures=full_text_captures,
        segments=segments,
        props=props,
        annotations=annotations,
        negative_evidence=negative_evidence,
        rival_explanations=rival_explanations,
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
        fixture_full_text_captures = _validate_file(
            fixture_dir / "full-text-captures.jsonl", FullTextCapture, report
        )
        fixture_segments = _validate_file(fixture_dir / "segments.jsonl", Segment, report)
        fixture_props = _validate_file(fixture_dir / "propositions.jsonl", Proposition, report)
        _validate_record_set(
            label=f"segmentation fixture {fixture_dir.name}",
            sources=fixture_sources,
            docs=fixture_docs,
            full_text_captures=fixture_full_text_captures,
            segments=fixture_segments,
            props=fixture_props,
            report=report,
        )
    return report
