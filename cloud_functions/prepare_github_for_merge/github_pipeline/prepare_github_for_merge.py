"""
Cloud Function Logic — Prepare GitHub Models for Merge
------------------------------------------------------
This function:
1. Reads mapped GitHub model metadata from GCS.
2. Normalizes it into a Hugging Face–aligned JSON list.
3. Writes the normalized list back to GCS as the "ready" file.

Environment variables:
- BUCKET_NAME: sunnysett-pipeline-output
- MAPPED_BLOB: github/mapped/github_mapped_data.json
- READY_BLOB:  github/ready_for_merge/github_ready_data.json
"""

import json
import os
from datetime import datetime
from google.cloud import storage


def normalize_model(model: dict) -> dict:
    """Normalize a single GitHub model entry into a Hugging Face–style record."""
    return {
        "modelId": model.get("modelId"),
        "author": model.get("author"),
        "pipeline_tag": model.get("task", "unknown"),
        "tags": model.get("topics", []) + ["source:github"],
        "library": model.get("language", "unknown"),
        "license": model.get("license", "unknown"),
        "downloads": model.get("downloads", None),
        "likes": model.get("stars", 0),
        "task": model.get("task", "unknown"),
        "categories": model.get("categories", []),
        "data_types": model.get("data_types", []),
        "repo_url": model.get("url", ""),
        "lastModified": model.get("lastModified", "unknown"),
        "private": model.get("private", False),
        "gated": model.get("gated", False),
        "safetensors": model.get("safetensors", False),
        "ingested_at": datetime.utcnow().isoformat() + "+00:00",
    }


def handle_request(request):
    """
    Main callable invoked by the HTTP Cloud Function.
    Downloads mapped data, normalizes it, and re-uploads the ready file.
    """
    try:
        # Load environment variables
        bucket_name = os.environ["BUCKET_NAME"]
        mapped_blob = os.environ["MAPPED_BLOB"]
        ready_blob = os.environ["READY_BLOB"]

        print(f"📦 Loading from: gs://{bucket_name}/{mapped_blob}")
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(mapped_blob)

        # Read JSON from GCS
        data = json.loads(blob.download_as_text())

        # Handle both structures: list or {"models": [...]}
        models = data.get("models", data) if isinstance(data, dict) else data
        if not isinstance(models, list):
            raise ValueError("Mapped file format invalid: expected list or {'models': list}")

        # Normalize all entries
        normalized = [normalize_model(m) for m in models]

        # Upload normalized data
        output_blob = bucket.blob(ready_blob)
        output_blob.upload_from_string(
            json.dumps(normalized, indent=2, ensure_ascii=False),
            content_type="application/json"
        )

        print(f"✅ Successfully processed {len(normalized)} models.")
        print(f"💾 Saved to: gs://{bucket_name}/{ready_blob}")

        return {"status": "success", "count": len(normalized)}

    except Exception as e:
        print(f"❌ Error in handle_request: {e}")
        return {"status": "error", "message": str(e)}
