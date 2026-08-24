from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .enums import CorpusTier, EvidenceDomain, EvidenceRelation, RecordStatus

SHA256 = r"^[a-f0-9]{64}$"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)


class Lineage(StrictModel):
    status: RecordStatus = RecordStatus.DRAFT
    version: str = "0.1.0"
    supersedes: list[str] = Field(default_factory=list)
    superseded_by: list[str] = Field(default_factory=list)
    change_note: str | None = None


class Source(StrictModel):
    source_id: str
    title: str
    source_kind: str
    corpus_tier: CorpusTier
    archival_citation: str | None = None
    bibliographic_citation: str | None = None
    canonical_url: str | None = None
    local_path: str | None = None
    source_location_name: str | None = None
    repository: str | None = None
    edition: str | None = None
    publication_date: date | None = None
    acquisition_date: date
    accessed_at: datetime
    capture_method: Literal[
        "manual_metadata_review",
        "downloaded_file",
        "static_html_scrape",
        "browser_rendered_capture",
        "ocr_text",
        "manual_transcription",
    ]
    checksum_sha256: str = Field(pattern=SHA256)
    checksum_scope: Literal["local_file", "remote_file", "metadata_record"]
    language: str
    original_language: str | None = None
    translation_status: Literal[
        "original_language",
        "human_translation",
        "machine_translation",
        "mixed_translation",
        "not_applicable",
        "unknown",
    ] = "unknown"
    translator: str | None = None
    translation_source_id: str | None = None
    translation_notes: str | None = None
    copyright_status: str
    redistribution_status: str
    source_reliability: Literal["high", "medium", "low", "uncertain"]
    provenance_notes: str | None = None
    lineage: Lineage = Field(default_factory=Lineage)


class Document(StrictModel):
    document_id: str
    source_id: str
    title: str
    document_date: date | None = None
    actor_ids: list[str] = Field(default_factory=list)
    audience: str | None = None
    evidence_domain: EvidenceDomain
    corpus_tier: CorpusTier
    case_id: str
    discourse_register: str | None = Field(default=None, alias="register")
    lineage: Lineage = Field(default_factory=Lineage)


class Segment(StrictModel):
    segment_id: str
    document_id: str
    segment_type: Literal["page", "paragraph", "sentence"]
    ordinal: int = Field(ge=1)
    text: str
    page_label: str | None = None
    char_start: int | None = Field(default=None, ge=0)
    char_end: int | None = Field(default=None, ge=0)
    text_hash: str = Field(pattern=SHA256)
    lineage: Lineage = Field(default_factory=Lineage)


class Proposition(StrictModel):
    proposition_id: str
    document_id: str
    segment_ids: list[str] = Field(min_length=1)
    exact_text: str
    char_start: int | None = Field(default=None, ge=0)
    char_end: int | None = Field(default=None, ge=0)
    proposition_note: str | None = None
    lineage: Lineage = Field(default_factory=Lineage)


class EvidenceLink(StrictModel):
    relation: EvidenceRelation
    proposition_ids: list[str] = Field(default_factory=list)
    negative_evidence_ids: list[str] = Field(default_factory=list)
    note: str | None = None


class RunOutput(StrictModel):
    path: str
    sha256: str = Field(pattern=SHA256)


class RunManifest(StrictModel):
    run_manifest_id: str
    command: str
    git_commit: str
    environment_lock_hash: str
    input_manifest_hashes: dict[str, str]
    schema_versions: dict[str, str]
    codebook_version: str
    model_runs: list[dict[str, Any]] = Field(default_factory=list)
    random_seeds: dict[str, int] = Field(default_factory=dict)
    started_at: datetime
    finished_at: datetime
    outputs: list[RunOutput] = Field(default_factory=list)
    status: Literal["success", "failed", "partial"]
