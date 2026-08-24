from pathlib import Path

from fspp_workbench.core.jsonl import read_jsonl
from fspp_workbench.core.models import Proposition, Segment
from fspp_workbench.projects.sacrificial_debt.models import (
    Annotation,
    NegativeEvidence,
    RivalExplanation,
)
from fspp_workbench.validation.repository import validate_project

DATA_ROOT = Path("projects/sacrificial-debt/data")


def test_reference_packet_records_validate() -> None:
    segments = [
        Segment.model_validate(record)
        for record in read_jsonl(DATA_ROOT / "segments.jsonl")
    ]
    propositions = [
        Proposition.model_validate(record)
        for record in read_jsonl(DATA_ROOT / "propositions.jsonl")
    ]
    annotations = [
        Annotation.model_validate(record)
        for record in read_jsonl(DATA_ROOT / "annotations" / "reference.jsonl")
    ]
    negative_evidence = [
        NegativeEvidence.model_validate(record)
        for record in read_jsonl(DATA_ROOT / "negative-evidence.jsonl")
    ]
    rival_explanations = [
        RivalExplanation.model_validate(record)
        for record in read_jsonl(DATA_ROOT / "rival-explanations.jsonl")
    ]

    assert len(segments) == 1
    assert len(propositions) == 1
    assert len(annotations) == 1
    assert len(negative_evidence) == 1
    assert len(rival_explanations) == 1
    assert segments[0].coordinate_scope == "segment_text"
    assert propositions[0].coordinate_scope == "segment_text"
    assert segments[0].locator_note == "Summary section, item 1, page 38."
    assert propositions[0].locator_note == "Summary section, item 1, page 38."
    assert annotations[0].coder_id == "project-owner"
    assert annotations[0].state == "observation_reviewed"
    assert negative_evidence[0].review_status == "reviewed"
    assert rival_explanations[0].review_status == "reviewed"


def test_reference_packet_is_included_in_repository_validation() -> None:
    report = validate_project(Path("."))

    assert report.ok, report.errors
