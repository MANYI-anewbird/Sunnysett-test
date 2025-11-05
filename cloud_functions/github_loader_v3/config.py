"""
Configuration for GitHub Loader v3
----------------------------------
"""

# Your GitHub personal access token
# Generate one at: https://github.com/settings/tokens (enable repo.read permission)
GITHUB_TOKEN = "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"

# Mock mode: True = skip real API calls and generate fake data
MOCK_MODE = False

# Repositories to extract (add as many as you want)
GITHUB_REPOS = [
    "karpathy/minGPT",
    "openai/gpt-2",
    "huggingface/transformers"
]
