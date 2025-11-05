"""
GitHub Loader - v2
功能：
1. 从 GitHub 提取 repo 的基础信息
2. 兼容新版 Github API（使用 auth=github.Auth.Token）
3. 自动保存到项目根目录下的 output/github_raw_data.json
"""

import os
import json
from pathlib import Path
from github import Github, Auth
from config import GITHUB_TOKEN, GITHUB_REPOS, MOCK_MODE

# 设置输出目录（在 Sunnysett-test/output 下）
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

def get_repo_basic_info(repo_name):
    """提取单个 repo 的基本信息"""
    if MOCK_MODE:
        print(f"  🔶 Mock use_test_data：{repo_name}")
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

    print(f"  🌐  GitHub API to get {repo_name} ...")
    try:
        auth = Auth.Token(GITHUB_TOKEN)
        g = Github(auth=auth)
        repo = g.get_repo(repo_name)

        data = {
            "modelId": repo.full_name,
            "author": repo.owner.login,
            "description": repo.description or "",
            "stars": repo.stargazers_count,
            "language": repo.language or "unknown",
            "topics": list(repo.get_topics()),
            "license": repo.license.spdx_id if repo.license else "unknown",
            "url": repo.html_url
        }

        print(f"  ✅ success to get (⭐ {data['stars']} stars)")
        return data

    except Exception as e:
        print(f"  ❌ fail to get: {e}")
        return None


def load_github_models():
    """批量加载多个 repo 信息"""
    print("\n" + "=" * 60)
    print("🚀 GitHub Loader - start extract")
    print("=" * 60)
    print(f"📋 in total {len(GITHUB_REPOS)} num_of_repo\n")

    all_data = []
    for i, repo_name in enumerate(GITHUB_REPOS, 1):
        print(f"📦 [{i}/{len(GITHUB_REPOS)}] {repo_name}")
        data = get_repo_basic_info(repo_name)
        if data:
            all_data.append(data)
        print()

    output_path = OUTPUT_DIR / "github_raw_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print("=" * 60)
    print(f"✅ success to get {len(all_data)} repos")
    print(f"💾 save to: {output_path}")
    print("=" * 60)

    return all_data


if __name__ == "__main__":
    data = load_github_models()
    if data:
        print("\n📊 sample data（first repo）：")
        print(json.dumps(data[0], indent=2, ensure_ascii=False))
