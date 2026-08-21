from __future__ import annotations

from datetime import date as DateType
from typing import Any, Literal

from pydantic import Field, model_validator

from fspp_workbench.core.models import Lineage, StrictModel

from .enums import (
    AnnotationState,
    CausalRole,
    DebtStatus,
    Dischargeability,
    EssentializationStatus,
    EvidenceStrength,
    ExplicitComparison,
    NegativeType,
)


class ObservationLayer(StrictModel):
    collective_object: str | None = None
    sacrificer_ids: list[str] = Field(default_factory=list)
    sacrifice_types: list[str] = Field(default_factory=list)
    alleged_survivor_ids: list[str] = Field(default_factory=list)
    explicit_comparison: ExplicitComparison
    moral_value_sacrifice: list[str] = Field(default_factory=list)
    moral_value_survival: list[str] = Field(default_factory=list)
    actor_ids: list[str] = Field(default_factory=list)
    audience: str | None = None
    date: DateType | None = None


class SacrificialAccounting(StrictModel):
    sacrificial_asymmetry: bool
    creditor_ids: list[str] = Field(default_factory=list)
    debtor_ids: list[str] = Field(default_factory=list)
    reciprocal_obligation: bool
    debt_status: DebtStatus = DebtStatus.ABSENT
    debt_language: list[str] = Field(default_factory=list)
    repayment_language: list[str] = Field(default_factory=list)
    equalization_claim: bool = False


class InterpretationLayer(StrictModel):
    accounting: SacrificialAccounting
    essentialization_status: EssentializationStatus = EssentializationStatus.NONE
    dischargeability: Dischargeability = Dischargeability.NOT_APPLICABLE
    sanction_types: list[str] = Field(default_factory=list)
    causal_role: CausalRole = CausalRole.UNCLEAR
    rival_explanation_ids: list[str] = Field(default_factory=list)
    evidence_strength: EvidenceStrength = EvidenceStrength.WEAK


class Annotation(StrictModel):
    annotation_id: str
    proposition_id: str
    state: AnnotationState
    observation: ObservationLayer
    interpretation: InterpretationLayer | None = None
    coder_id: str
    codebook_version: str
    lineage: Lineage = Field(default_factory=Lineage)

    @model_validator(mode="after")
    def enforce_state_separation(self) -> Annotation:
        interpretation_states = {
            AnnotationState.INTERPRETATION_DRAFT,
            AnnotationState.REFERENCE_REVIEWED,
            AnnotationState.RELEASED,
        }
        if self.state not in interpretation_states and self.interpretation is not None:
            raise ValueError("Interpretation is forbidden until observation is locked")
        if self.state in interpretation_states and self.interpretation is None:
            raise ValueError("Interpretation is required after observation lock")
        return self

    @model_validator(mode="after")
    def enforce_minimum_debt_rule(self) -> Annotation:
        if not self.interpretation:
            return self
        a = self.interpretation.accounting
        if self.interpretation.evidence_strength in {
            EvidenceStrength.STRONG,
            EvidenceStrength.DECISIVE_FOR_MECHANISM,
        }:
            if not self.observation.sacrifice_types:
                raise ValueError("Strong debt evidence requires identifiable sacrifice")
            if self.observation.explicit_comparison != ExplicitComparison.YES:
                raise ValueError("Strong debt evidence requires explicit comparison")
            if not a.reciprocal_obligation:
                raise ValueError("Strong debt evidence requires normative reciprocal obligation")
        return self


class SearchScope(StrictModel):
    corpus_tiers: list[str]
    source_families: list[str] = Field(default_factory=list)
    date_range: str | None = None
    terms: list[str] = Field(default_factory=list)
    query_or_protocol: str


class NegativeEvidence(StrictModel):
    negative_evidence_id: str
    case_id: str
    proposition_ids: list[str] = Field(default_factory=list)
    negative_type: NegativeType
    hypothesis_ids: list[str] = Field(default_factory=list)
    falsification_test_ids: list[str] = Field(default_factory=list)
    search_scope: SearchScope | None = None
    strength: Literal["weak", "moderate", "strong", "decisive_for_test"]
    implication: str
    review_status: Literal["draft", "reviewed", "adjudicated"] = "draft"

    @model_validator(mode="after")
    def absence_requires_search_scope(self) -> NegativeEvidence:
        if (
            self.negative_type == NegativeType.EXPECTED_RHETORIC_ABSENT
            and self.search_scope is None
        ):
            raise ValueError("Absence claims require a documented search_scope")
        return self


class RivalExplanation(StrictModel):
    rival_explanation_id: str
    proposition_id: str | None = None
    explanation_type: str
    support_status: Literal["supported", "plausible", "weak", "contradicted", "not_assessed"]
    evidence_refs: list[str] = Field(default_factory=list)
    interaction_with_sacrificial_debt: Literal[
        "independent", "complementary", "mediating", "competing", "unknown"
    ] = "unknown"
    notes: str | None = None


class Adjudication(StrictModel):
    adjudication_id: str
    unit_id: str
    field_name: str
    coder_values: dict[str, Any]
    decision: Literal["accept_a", "accept_b", "synthesize", "uncertain", "exclude", "defer"]
    adjudicated_value: Any | None = None
    rationale: str
    codebook_change_needed: bool = False
    correction_candidate: bool = False
    adjudicator_id: str
    date: DateType


class EvidenceChain(StrictModel):
    evidence_chain_id: str
    claim_id: str
    mechanism_component_ids: list[str] = Field(default_factory=list)
    supporting_proposition_ids: list[str] = Field(default_factory=list)
    contradicting_proposition_ids: list[str] = Field(default_factory=list)
    qualifying_proposition_ids: list[str] = Field(default_factory=list)
    negative_evidence_ids: list[str] = Field(default_factory=list)
    rival_explanation_ids: list[str] = Field(default_factory=list)
    case_ids: list[str] = Field(min_length=1)
    source_quality_summary: dict[str, Any] = Field(default_factory=dict)
    chain_strength: EvidenceStrength
    review_status: Literal["draft", "human_reviewed", "publication_locked"] = "draft"


class ResearchClaim(StrictModel):
    claim_id: str
    claim_text: str
    claim_type: Literal["descriptive", "interpretive", "comparative", "causal"]
    causal_role: CausalRole | None = None
    scope_cases: list[str] = Field(min_length=1)
    scope_period: dict[str, Any] | None = None
    evidence_chain_ids: list[str] = Field(min_length=1)
    rival_explanation_ids: list[str] = Field(default_factory=list)
    evidence_strength: EvidenceStrength
    human_review_status: Literal["pending", "passed", "failed"] = "pending"
    model_stress_status: Literal["not_run", "passed", "concerns"] = "not_run"
    version: str
    change_note: str | None = None
    status: Literal["draft", "active", "narrowed", "rejected", "superseded"] = "draft"
