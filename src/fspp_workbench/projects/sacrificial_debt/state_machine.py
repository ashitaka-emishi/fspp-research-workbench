from .enums import AnnotationState

ALLOWED_TRANSITIONS: dict[AnnotationState, set[AnnotationState]] = {
    AnnotationState.OBSERVATION_DRAFT: {AnnotationState.OBSERVATION_REVIEWED},
    AnnotationState.OBSERVATION_REVIEWED: {
        AnnotationState.OBSERVATION_DRAFT,
        AnnotationState.OBSERVATION_LOCKED,
    },
    AnnotationState.OBSERVATION_LOCKED: {AnnotationState.INTERPRETATION_DRAFT},
    AnnotationState.INTERPRETATION_DRAFT: {AnnotationState.REFERENCE_REVIEWED},
    AnnotationState.REFERENCE_REVIEWED: {
        AnnotationState.INTERPRETATION_DRAFT,
        AnnotationState.RELEASED,
    },
    AnnotationState.RELEASED: set(),
}


def can_transition(current: AnnotationState, target: AnnotationState) -> bool:
    return target in ALLOWED_TRANSITIONS[current]


def assert_transition(current: AnnotationState, target: AnnotationState) -> None:
    if not can_transition(current, target):
        raise ValueError(f"Illegal annotation transition: {current} -> {target}")
