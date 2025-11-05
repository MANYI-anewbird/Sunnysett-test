import os, json
from github_pipeline.github_loader import load_github_models
from google.cloud import storage

OUTPUT_DIR = "../output"
BUCKET_NAME = "sunnysett-pipeline-output"

def upload_to_gcs(bucket_name, file_path, blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_path)
    print(f"✅ Uploaded {file_path} → gs://{bucket_name}/{blob_name}")

def run_pipeline():
    data = load_github_models()
    output_file = os.path.join(OUTPUT_DIR, "semantic_models_github.json")
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    upload_to_gcs(BUCKET_NAME, output_file, "semantic_models_github.json")

if __name__ == "__main__":
    run_pipeline()
