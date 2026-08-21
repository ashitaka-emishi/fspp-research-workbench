from enum import StrEnum


class AnnotationState(StrEnum):
    OBSERVATION_DRAFT = "observation_draft"
    OBSERVATION_REVIEWED = "observation_reviewed"
    OBSERVATION_LOCKED = "observation_locked"
    INTERPRETATION_DRAFT = "interpretation_draft"
    REFERENCE_REVIEWED = "reference_reviewed"
    RELEASED = "released"


class ExplicitComparison(StrEnum):
    YES = "yes"
    NO = "no"
    UNCERTAIN = "uncertain"


class DebtStatus(StrEnum):
    EMIC = "emic"
    ETIC = "etic"
    MIXED = "mixed"
    ABSENT = "absent"


class EssentializationStatus(StrEnum):
    INDIVIDUAL_BEHAVIOR = "individual_behavior"
    GROUP_GENERALIZED = "group_generalized"
    RACIAL_ONTOLOGICAL = "racial_ontological"
    OTHER_ONTOLOGICAL = "other_ontological"
    UNCLEAR = "unclear"
    NONE = "none"


class Dischargeability(StrEnum):
    DISCHARGEABLE = "dischargeable"
    CONTESTED = "contested"
    NON_DISCHARGEABLE = "non_dischargeable"
    UNCLEAR = "unclear"
    NOT_APPLICABLE = "not_applicable"


class CausalRole(StrEnum):
    CONSTITUTIVE = "constitutive"
    DIAGNOSTIC = "diagnostic"
    MOTIVATIONAL = "motivational"
    LEGITIMATING = "legitimating"
    ESCALATORY = "escalatory"
    DECISION_CAUSAL = "decision_causal"
    UNCLEAR = "unclear"


class EvidenceStrength(StrEnum):
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    DECISIVE_FOR_MECHANISM = "decisive_for_mechanism"


class NegativeType(StrEnum):
    DISCHARGE_SUCCESS = "discharge_success"
    VETERAN_PROTECTION = "veteran_protection"
    CONTRIBUTION_RECLASSIFICATION = "contribution_reclassification"
    EXPECTED_RHETORIC_ABSENT = "expected_rhetoric_absent"
    COERCION_WITHOUT_DEBT = "coercion_without_debt"
    DEBT_WITHOUT_COERCION = "debt_without_coercion"
    EXPLICIT_REJECTION = "explicit_rejection"
    CHRONOLOGY_CONTRADICTION = "chronology_contradiction"
    ACTOR_INCONSISTENCY = "actor_inconsistency"
    OTHER = "other"
