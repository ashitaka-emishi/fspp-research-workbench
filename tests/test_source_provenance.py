import json
from pathlib import Path

from fspp_workbench.core.hashing import sha256_text
from fspp_workbench.core.jsonl import read_jsonl
from fspp_workbench.core.models import Source


def test_seed_source_metadata_checksums_are_stable() -> None:
    path = Path("projects/sacrificial-debt/data/sources.jsonl")
    records = read_jsonl(path)
    assert records

    for record in records:
        source = Source.model_validate(record)
        assert source.corpus_tier
        assert source.accessed_at
        assert source.capture_method
        assert source.redistribution_status
        assert source.translation_status
        if source.canonical_url:
            assert source.source_location_name
        if source.translation_status == "original_language":
            assert source.original_language == source.language
        if source.translation_status in {
            "human_translation",
            "machine_translation",
            "mixed_translation",
        }:
            assert source.original_language
        if source.checksum_scope in {"local_file", "remote_file"}:
            assert source.canonical_url
        if source.checksum_scope == "metadata_record":
            payload = {key: value for key, value in record.items() if key != "checksum_sha256"}
            text = json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
            assert source.checksum_sha256 == sha256_text(text)
