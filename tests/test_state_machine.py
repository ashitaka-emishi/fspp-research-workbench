import pytest

from fspp_workbench.projects.sacrificial_debt.enums import AnnotationState
from fspp_workbench.projects.sacrificial_debt.state_machine import assert_transition


def test_cannot_skip_observation_lock() -> None:
    with pytest.raises(ValueError):
        assert_transition(AnnotationState.OBSERVATION_DRAFT, AnnotationState.INTERPRETATION_DRAFT)
