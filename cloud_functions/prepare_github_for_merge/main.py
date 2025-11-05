"""
Entrypoint for Cloud Function: prepare-github-for-merge
-------------------------------------------------------
HTTP-triggered wrapper that calls the normalization logic.
"""

from flask import jsonify, Request
from github_pipeline.prepare_github_for_merge import handle_request


def main(request: Request):
    try:
        print("🚀 Received HTTP request for GitHub-to-HuggingFace normalization")
        result = handle_request(request)
        return jsonify(result)
    except Exception as e:
        print(f"❌ Cloud Function crashed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
