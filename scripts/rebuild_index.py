#!/usr/bin/env python3
"""Rebuild index.json from image files and optional metadata.json."""
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
STICKERS = ROOT / "stickers"
EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
BASE_URL = "https://raw.githubusercontent.com/tusumy/biaoqing/main/"
metadata = json.loads((ROOT / "metadata.json").read_text(encoding="utf-8"))
items = []
for image in sorted(STICKERS.rglob("*")):
    if not image.is_file() or image.suffix.lower() not in EXTENSIONS:
        continue
    rel = image.relative_to(ROOT).as_posix()
    key = image.stem
    meta = metadata.get(key, {})
    items.append({
        "id": key,
        "title": meta.get("title", key),
        "tags": meta.get("tags", []),
        "path": rel,
        "url": BASE_URL + quote(rel),
    })
index = {"version": 1, "count": len(items), "stickers": items}
(ROOT / "index.json").write_text(
    json.dumps(index, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(f"Indexed {len(items)} stickers")
