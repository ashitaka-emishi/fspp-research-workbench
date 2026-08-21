import pytest
from pydantic import ValidationError

from fspp_workbench.projects.sacrificial_debt.models import NegativeEvidence


def test_absence_claim_requires_search_scope() -> None:
    with pytest.raises(ValidationError):
        NegativeEvidence.model_validate({
            "negative_evidence_id":"sd-neg-000001", "case_id":"sd-case-germany",
            "negative_type":"expected_rhetoric_absent", "strength":"moderate",
            "implication":"Synthetic test implication"
        })
