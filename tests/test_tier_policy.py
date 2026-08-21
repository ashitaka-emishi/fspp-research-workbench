import pytest

from fspp_workbench.core.enums import CorpusTier
from fspp_workbench.core.tier_policy import TierPolicyError, assert_claim_eligible


def test_tier3_is_never_claim_evidence() -> None:
    with pytest.raises(TierPolicyError):
        assert_claim_eligible(CorpusTier.TIER3, strong_interpretive_claim=False)


def test_strong_claim_requires_tier1() -> None:
    with pytest.raises(TierPolicyError):
        assert_claim_eligible(CorpusTier.TIER2, strong_interpretive_claim=True)
