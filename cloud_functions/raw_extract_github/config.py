"""
"""
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "output"
DATA_DIR = PROJECT_ROOT / "data"

OUTPUT_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)


GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


GITHUB_REPOS = [
    "karpathy/minGPT",
    "ultralytics/yolov5",
    "facebookresearch/segment-anything"
]

BUCKET_NAME = "sunnysett-pipeline-output"


FILE_PATTERNS = {
    "python": [".py"],
    "markdown": [".md"],
    "requirements": ["requirements.txt"]
}

MOCK_MODE = False  # 