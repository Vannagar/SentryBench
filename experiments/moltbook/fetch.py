"""Download the Moltbook files needed for the influence graph, with a progress bar.

Run from the repo root:
    python experiments/moltbook/fetch.py

Saves to data/moltbook/ (git-ignored). Skips files that are already complete.
Source: https://huggingface.co/datasets/DavidTKeane/moltbook-ai-injection-dataset (CC-BY-4.0)
"""

import sys
import urllib.request
from pathlib import Path

BASE = "https://huggingface.co/datasets/DavidTKeane/moltbook-ai-injection-dataset/resolve/main/"
FILES = [
    "injections_found.json",         # ~4 MB: 4,209 flagged hijack attempts
    "all_posts_with_comments.json",  # ~105 MB: every post with its comment thread
]
OUT = Path("data/moltbook")


def fetch(name: str) -> None:
    dest = OUT / name
    with urllib.request.urlopen(BASE + name, timeout=60) as r:
        total = int(r.headers.get("Content-Length", 0))
        if dest.exists() and dest.stat().st_size == total:
            print(f"{name}: already downloaded")
            return
        done = 0
        tmp = dest.with_suffix(".part")
        with open(tmp, "wb") as f:
            while chunk := r.read(1 << 20):
                f.write(chunk)
                done += len(chunk)
                pct = 100 * done / total if total else 0
                bar = "#" * int(pct // 4)
                sys.stdout.write(f"\r{name}: [{bar:<25}] {pct:5.1f}%  {done / 1e6:6.1f} / {total / 1e6:.1f} MB")
                sys.stdout.flush()
        tmp.rename(dest)
        print()


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        fetch(name)
    print(f"Done. Files are in {OUT}/")
