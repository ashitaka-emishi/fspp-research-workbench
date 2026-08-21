import pytest
from pydantic import ValidationError

from fspp_workbench.projects.sacrificial_debt.models import Annotation

OBS = {
    "collective_object": "synthetic collective",
    "sacrificer_ids": ["actor-a"],
    "sacrifice_types": ["military_service"],
    "alleged_survivor_ids": ["actor-b"],
    "explicit_comparison": "yes",
    "moral_value_sacrifice": ["duty"],
    "moral_value_survival": ["undeserved"],
}

INTERP = {
    "accounting": {
        "sacrificial_asymmetry": True,
        "creditor_ids": ["actor-a"],
        "debtor_ids": ["actor-b"],
        "reciprocal_obligation": True,
        "debt_status": "emic"
    },
    "essentialization_status": "group_generalized",
    "dischargeability": "contested",
    "sanction_types": ["stigma"],
    "causal_role": "legitimating",
    "evidence_strength": "strong"
}


def test_interpretation_forbidden_before_observation_lock() -> None:
    with pytest.raises(ValidationError):
        Annotation.model_validate({
            "annotation_id":"sd-ann-000001", "proposition_id":"sd-prop-000001",
            "state":"observation_draft", "observation":OBS, "interpretation":INTERP,
            "coder_id":"coder-a", "codebook_version":"0.2.0"
        })


def test_strong_debt_requires_explicit_comparison() -> None:
    bad_obs = {**OBS, "explicit_comparison":"no"}
    with pytest.raises(ValidationError):
        Annotation.model_validate({
            "annotation_id":"sd-ann-000001", "proposition_id":"sd-prop-000001",
            "state":"reference_reviewed", "observation":bad_obs, "interpretation":INTERP,
            "coder_id":"coder-a", "codebook_version":"0.2.0"
        })


def test_valid_strong_annotation() -> None:
    record = Annotation.model_validate({
        "annotation_id":"sd-ann-000001", "proposition_id":"sd-prop-000001",
        "state":"reference_reviewed", "observation":OBS, "interpretation":INTERP,
        "coder_id":"coder-a", "codebook_version":"0.2.0"
    })
    assert record.interpretation is not None
