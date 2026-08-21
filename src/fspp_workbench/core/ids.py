import re
from dataclasses import dataclass

ID_RE = re.compile(r"^[a-z][a-z0-9-]*-[a-z][a-z0-9-]*-[0-9]{6}$")


@dataclass(frozen=True)
class StableId:
    project: str
    entity: str
    number: int

    def __str__(self) -> str:
        return f"{self.project}-{self.entity}-{self.number:06d}"


def make_id(project: str, entity: str, number: int) -> str:
    if number < 1:
        raise ValueError("Stable ID number must be >= 1")
    value = str(StableId(project, entity, number))
    if not ID_RE.match(value):
        raise ValueError(f"Invalid stable ID components: {value}")
    return value


def validate_id(value: str) -> str:
    if not ID_RE.match(value):
        raise ValueError(f"Not a FSPP Research Workbench stable ID: {value}")
    return value
