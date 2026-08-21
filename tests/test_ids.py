import pytest

from fspp_workbench.core.ids import make_id, validate_id


def test_make_stable_id() -> None:
    assert make_id("sd", "prop", 1) == "sd-prop-000001"


def test_invalid_id_rejected() -> None:
    with pytest.raises(ValueError):
        validate_id("doc_001")
