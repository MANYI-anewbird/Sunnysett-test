"""
Cloud Function: map-github-taxonomy (HTTP)
------------------------------------------
Reads raw GitHub models JSON from GCS, maps taxonomy using local pipeline,
and writes the mapped JSON back to GCS under github/mapped/.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone
from google.cloud import storage

# import your local pipeline modules (copied with the function)
from github_pipeline.taxonomy_mapper import map_models

# === Config via env (with sane defaults) ===
BUCKET_NAME = os.environ.get("BUCKET_NAME", "sunnysett-pipeline-output")
RAW_BLOB = os.environ.get("RAW_BLOB", "github/raw/github_raw_data.json")
MAPPED_BLOB = os.environ.get("MAPPED_BLOB", "github/mapped/github_mapped_data.json")

LOCAL_RAW = Path("/tmp/github_raw_data.json")
LOCAL_MAPPED = Path("/tmp/github_mapped_data.json")


def _download_from_gcs(bucket: str, blob: str, local_path: Path) -> None:
    client = storage.Client()
    bkt = client.bucket(bucket)
    obj = bkt.blob(blob)
    if not obj.exists():
        raise FileNotFoundError(f"gs://{bucket}/{blob} not found")
    local_path.parent.mkdir(parents=True, exist_ok=True)
    obj.download_to_filename(str(local_path))


def _upload_to_gcs(bucket: str, blob: str, local_path: Path) -> None:
    client = storage.Client()
    bkt = client.bucket(bucket)
    obj = bkt.blob(blob)
    obj.upload_from_filename(str(local_path))


def main(request):
    """
    HTTP entrypoint.
    Optional JSON body overrides:
      {
        "bucket": "...",
        "raw_blob": "...",
        "mapped_blob": "..."
      }
    """
    try:
        body = {}
        try:
            body = request.get_json(silent=True) or {}
        except Exception:
            body = {}

        bucket = body.get("bucket", BUCKET_NAME)
        raw_blob = body.get("raw_blob", RAW_BLOB)
        mapped_blob = body.get("mapped_blob", MAPPED_BLOB)

        print(f"Reading: gs://{bucket}/{raw_blob}")
        _download_from_gcs(bucket, raw_blob, LOCAL_RAW)

        with open(LOCAL_RAW, "r", encoding="utf-8") as f:
            raw_models = json.load(f)

        # Map taxonomy
        mapped = map_models(raw_models)

        # Stamp a run metadata block
        out = {
            "metadata": {
                "source": f"gs://{bucket}/{raw_blob}",
                "generated_at": datetime.now(timezone.utc).isoformat()
            },
            "models": mapped
        }

        with open(LOCAL_MAPPED, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)

        _upload_to_gcs(bucket, mapped_blob, LOCAL_MAPPED)

        msg = {
            "status": "success",
            "bucket": bucket,
            "mapped_blob": mapped_blob,
            "count": len(mapped)
        }
        print(msg)
        return (json.dumps(msg), 200, {"Content-Type": "application/json"})

    except Exception as e:
        err = {"status": "error", "message": str(e)}
        print(err)
        return (json.dumps(err), 500, {"Content-Type": "application/json"})
