"""
GitHub Loader - v3 (Scalable version)
------------------------------------
Features:
1. Extracts repo metadata from GitHub API
2. Supports checkpointing (each repo saved individually)
3. Automatically merges all files into github_raw_v3_data.json
"""

import os
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from github import Github, Auth
from config import GITHUB_TOKEN, GITHUB_REPOS, MOCK_MODE


# Output directories
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "output" / "github_raw_v3"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MERGED_FILE = OUTPUT_DIR.parents[0] / "github_raw_v3_data.json"


def get_repo_basic_info(repo_name):
    """Extract metadata for a single repository."""
    if MOCK_MODE:
        print(f"🔶 Mock mode enabled: {repo_name}")
        return {
            "modelId": repo_name,
            "author": repo_name.split("/")[0],
            "description": f"Mock description for {repo_name}",
            "stars": 1000,
            "language": "Python",
            "topics": ["mock", "test"],
            "license": "MIT",
            "url": f"https://github.com/{repo_name}"
        }

    try:
        auth = Auth.Token(GITHUB_TOKEN)
        g = Github(auth=auth)
        repo = g.get_repo(repo_name)

        return {
            "modelId": repo.full_name,
            "author": repo.owner.login,
            "description": repo.description or "",
            "stars": repo.stargazers_count,
            "language": repo.language or "unknown",
            "topics": list(repo.get_topics()),
            "license": repo.license.spdx_id if repo.license else "unknown",
            "url": repo.html_url,
            "task": "unknown"
        }

    except Exception as e:
        print(f"❌ Failed to fetch {repo_name}: {e}")
        return None


def process_repo(repo_name):
    """Handle extraction + caching for a single repo."""
    save_path = OUTPUT_DIR / f"{repo_name.replace('/', '__')}.json"
    if save_path.exists():
        return f"🟡 Skipped (already exists): {repo_name}"

    data = get_repo_basic_info(repo_name)
    if data:
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return f"✅ Saved successfully: {repo_name}"
    else:
        return f"❌ Failed: {repo_name}"


def merge_raw_files():
    """Combine all individual repo JSON files."""
    all_files = list(OUTPUT_DIR.glob("*.json"))
    data = []
    for f in all_files:
        try:
            with open(f, "r", encoding="utf-8") as j:
                data.append(json.load(j))
        except Exception:
            print(f"⚠️ Skipping corrupted file: {f}")
    with open(MERGED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Merged {len(data)} repos → {MERGED_FILE}")


def load_github_models(max_workers=10):
    """Run parallel GitHub extraction."""
    print(f"\n🚀 Starting extraction for {len(GITHUB_REPOS)} repositories...\n")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_repo, r) for r in GITHUB_REPOS]
        for f in as_completed(futures):
            print(f.result())

    merge_raw_files()
    print("\n✅ All tasks completed.")


if __name__ == "__main__":
    load_github_models()
