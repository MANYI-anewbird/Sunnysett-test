"""
Cloud Function: raw-extract-github (pure GCF style)
---------------------------------------------------
Extracts GitHub repository metadata using the GitHub API,
saves locally, and uploads it to Google Cloud Storage.
"""

import os
import json
from pathlib import Path
from github_pipeline.github_loader import load_github_models
from google.cloud import storage

BUCKET_NAME = "sunnysett-pipeline-output"
DESTINATION_BLOB = "github/raw/github_raw_data.json"
LOCAL_OUTPUT_PATH = Path("/tmp/github_raw_data.json")

def upload_to_gcs(local_path: Path, bucket_name: str, destination_blob: str):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(local_path)
    print(f"☁️ Uploaded to gs://{bucket_name}/{destination_blob}")

def main(request):
    """HTTP Cloud Function entrypoint"""
    print("🚀 Starting GitHub extraction...")

    try:
        data = load_github_models()
        print(f"✅ Loaded {len(data)} repos")

        with open(LOCAL_OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        upload_to_gcs(LOCAL_OUTPUT_PATH, BUCKET_NAME, DESTINATION_BLOB)
        print("✅ Upload completed")

        return (json.dumps({"status": "success", "count": len(data)}), 200, {"Content-Type": "application/json"})

    except Exception as e:
        print(f"❌ Exception: {e}")
        return (json.dumps({"status": "error", "message": str(e)}), 500, {"Content-Type": "application/json"})

