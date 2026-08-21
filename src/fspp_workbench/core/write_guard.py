from pathlib import Path

CANONICAL_RELEASE_MARKER = ".released"


def assert_writable(path: Path) -> None:
    """Refuse mutation below a directory marked as released.

    A release workflow may place `.released` at a canonical data root. Corrections then
    require a superseding record or a new release workspace rather than destructive edit.
    """
    current = path.resolve()
    for parent in [current, *current.parents]:
        if (parent / CANONICAL_RELEASE_MARKER).exists():
            raise PermissionError(
                f"Refusing to mutate released canonical data below {parent}. "
                "Create a superseding record/new release instead."
            )
