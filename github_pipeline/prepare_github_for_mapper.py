"""
Prepare GitHub Models for Unified Schema (v2)
-------------------------------------------------
This script normalizes GitHub-extracted model metadata
into a Hugging Face–compatible format.
It fills in missing fields (downloads, private, gated, etc.)
and ensures consistent field naming for dataset merging.
"""

import json
from datetime import datetime
from pathlib import Path


def normalize_github_model(model: dict) -> dict:
    """
    Map GitHub model fields to Hugging Face–style format.
    """
    return {
        "modelId": model.get("modelId"),
        "author": model.get("author"),
        "pipeline_tag": model.get("task", "unknown"),
        "tags": model.get("topics", []) + ["source:github"],
        "library": model.get("language", "unknown"),
        "license": model.get("license", "unknown"),
        "downloads": None,
        "likes": model.get("stars", 0),
        "task": model.get("task", "unknown"),
        "categories": model.get("categories", []),
        "data_types": model.get("data_types", []),
        "repo_url": model.get("url", ""),
        "lastModified": "unknown",
        "private": False,
        "gated": False,
        "safetensors": False,
        "ingested_at": datetime.utcnow().isoformat() + "+00:00",
    }


def prepare_github_models(input_path: Path, output_path: Path):
    """
    Read mapped GitHub models and export them
    in a unified Hugging Face–compatible JSON format.
    """
    print("\n" + "=" * 60)
    print("🧭 Prepare GitHub Models - Normalizing to Hugging Face format")
    print("=" * 60)

    with open(input_path, "r", encoding="utf-8") as f:
        models = json.load(f)

    normalized = [normalize_github_model(m) for m in models]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(normalized, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved normalized data: {output_path}")
    print(f"📊 Total models processed: {len(normalized)}")
    print("=" * 60)
    return normalized


if __name__ == "__main__":
    input_path = Path(__file__).resolve().parents[1] / "output/github_mapped_data.json"
    output_path = Path(__file__).resolve().parents[1] / "output/github_ready_for_merge.json"

    prepare_github_models(input_path, output_path)
