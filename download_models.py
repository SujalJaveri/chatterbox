"""
Model Weights Downloader & Verifier for Chatterbox Turbo TTS
Ensures all required neural model weights and tokenizer configurations
are downloaded locally to the Hugging Face cache directory.
"""

import os
import sys
import urllib.request
from pathlib import Path

SNAPSHOT_ID = "749d1c1a46eb10492095d68fbcf55691ccf137cd"
CACHE_DIR = (
    Path.home()
    / ".cache"
    / "huggingface"
    / "hub"
    / "models--ResembleAI--chatterbox-turbo"
    / "snapshots"
    / SNAPSHOT_ID
)

BASE_CDN_URL = "https://huggingface.co/ResembleAI/chatterbox-turbo/resolve/main"

REQUIRED_FILES = {
    "added_tokens.json": 418,
    "conds.pt": 169454,
    "merges.txt": 456318,
    "special_tokens_map.json": 470,
    "tokenizer_config.json": 3878,
    "vocab.json": 999186,
    "t3_turbo_v1.yaml": 8457,
    "ve.safetensors": 5695784,
    "s3gen_meanflow.safetensors": 1064875036,
    "t3_turbo_v1.safetensors": 1915480052,
}


def download_file(url: str, dest_path: Path, expected_size: int = None):
    """Downloads a file with progress display."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = dest_path.with_suffix(dest_path.suffix + ".part")

    print(f"Downloading: {dest_path.name}...")
    headers = {"User-Agent": "Chatterbox-TTS-Launcher/1.0"}

    # Resume support if partial file exists
    initial_bytes = 0
    if temp_path.exists():
        initial_bytes = temp_path.stat().st_size
        headers["Range"] = f"bytes={initial_bytes}-"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response, open(
            temp_path, "ab" if initial_bytes else "wb"
        ) as f:
            total = expected_size or int(response.headers.get("Content-Length", 0)) + initial_bytes
            downloaded = initial_bytes
            chunk_size = 1024 * 1024  # 1MB chunks

            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                percent = (downloaded / total * 100) if total else 0
                mb_down = downloaded / (1024 * 1024)
                mb_total = total / (1024 * 1024) if total else 0
                print(
                    f"\r  [{percent:5.1f}%] {mb_down:6.1f}MB / {mb_total:6.1f}MB",
                    end="",
                    flush=True,
                )
        print()
        if temp_path.exists():
            if dest_path.exists():
                dest_path.unlink()
            temp_path.rename(dest_path)
        print(f"  [OK] Saved {dest_path.name}")
    except Exception as e:
        print(f"\n  [ERROR] Failed to download {dest_path.name}: {e}")
        raise


def ensure_models() -> Path:
    """Verifies all weights exist; downloads any missing ones."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    missing = []
    for fname, exp_size in REQUIRED_FILES.items():
        fpath = CACHE_DIR / fname
        if not fpath.exists() or (exp_size and fpath.stat().st_size < exp_size * 0.99):
            missing.append(fname)

    if not missing:
        return CACHE_DIR

    print(f"Found {len(missing)} model files to download...")
    for fname in missing:
        url = f"{BASE_CDN_URL}/{fname}"
        dest = CACHE_DIR / fname
        download_file(url, dest, REQUIRED_FILES[fname])

    print("All Chatterbox model checkpoints verified!")
    return CACHE_DIR


if __name__ == "__main__":
    ensure_models()
