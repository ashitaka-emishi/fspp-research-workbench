from pathlib import Path

import pytest

from fspp_workbench.core.write_guard import assert_writable


def test_released_tree_is_immutable(tmp_path: Path) -> None:
    root = tmp_path / "canonical"
    target = root / "annotations" / "reference.jsonl"
    target.parent.mkdir(parents=True)
    (root / ".released").write_text("release", encoding="utf-8")
    with pytest.raises(PermissionError):
        assert_writable(target)
