import json
from pathlib import Path

from fspp_workbench.core.models import Document, Proposition, RunManifest, Segment, Source
from fspp_workbench.projects.sacrificial_debt.models import (
    Adjudication,
    Annotation,
    EvidenceChain,
    NegativeEvidence,
    ResearchClaim,
)

MODELS = {
    "source": Source,
    "document": Document,
    "segment": Segment,
    "proposition": Proposition,
    "run-manifest": RunManifest,
    "sd-annotation": Annotation,
    "sd-negative-evidence": NegativeEvidence,
    "sd-evidence-chain": EvidenceChain,
    "sd-research-claim": ResearchClaim,
    "sd-adjudication": Adjudication,
}


def render_schemas(target: Path) -> dict[str, str]:
    target.mkdir(parents=True, exist_ok=True)
    rendered: dict[str, str] = {}
    for name, model in MODELS.items():
        text = json.dumps(model.model_json_schema(), indent=2, sort_keys=True) + "\n"
        (target / f"{name}.schema.json").write_text(text, encoding="utf-8")
        rendered[name] = text
    return rendered
