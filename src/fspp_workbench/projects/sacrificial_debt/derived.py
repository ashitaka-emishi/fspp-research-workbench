from .enums import DebtStatus, EssentializationStatus
from .models import Annotation


def derive_sacrificial_framing(annotation: Annotation) -> int:
    """Derive prospectus v0.2 framing level 0-5.

    Equalization meaning is retained as an independent structured field rather than silently
    introducing a sixth level. A codebook revision may change this function later.
    """
    obs = annotation.observation
    interp = annotation.interpretation
    if interp is None:
        return 1 if obs.sacrifice_types else 0
    acct = interp.accounting
    if interp.dischargeability.value == "non_dischargeable":
        return 5
    if interp.essentialization_status in {
        EssentializationStatus.GROUP_GENERALIZED,
        EssentializationStatus.RACIAL_ONTOLOGICAL,
        EssentializationStatus.OTHER_ONTOLOGICAL,
    } and acct.debt_status != DebtStatus.ABSENT:
        return 4
    if acct.reciprocal_obligation:
        return 3
    if acct.sacrificial_asymmetry:
        return 2
    if obs.sacrifice_types:
        return 1
    return 0
