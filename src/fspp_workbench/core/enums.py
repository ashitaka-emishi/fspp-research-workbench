from enum import StrEnum


class CorpusTier(StrEnum):
    TIER1 = "tier1"
    TIER2 = "tier2"
    TIER3 = "tier3"


class EvidenceDomain(StrEnum):
    RHETORIC = "rhetoric"
    RECEPTION = "reception"
    POLICY = "policy"


class RecordStatus(StrEnum):
    DRAFT = "draft"
    REVIEWED = "reviewed"
    RELEASED = "released"
    SUPERSEDED = "superseded"
    DEPRECATED = "deprecated"


class EvidenceRelation(StrEnum):
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    QUALIFIES = "qualifies"
