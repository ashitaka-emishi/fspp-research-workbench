from .enums import CorpusTier


class TierPolicyError(ValueError):
    pass


def assert_claim_eligible(tier: CorpusTier, *, strong_interpretive_claim: bool) -> None:
    if tier == CorpusTier.TIER3:
        raise TierPolicyError("Tier 3 search/reference hits are leads, not coded claim evidence")
    if strong_interpretive_claim and tier != CorpusTier.TIER1:
        raise TierPolicyError("Strong interpretive/causal claims require Tier 1 evidence")
