#!/usr/bin/env python3
import argparse
import json
import re
import time
from pathlib import Path
from typing import Any, Dict, List

from src.firecrawl_client.client import FirecrawlClient
from src.utils.config import settings
from src.utils.io import ensure_dir, write_json


def _sanitize_for_filename(value: str) -> str:
    v = (value or "").strip().lower()
    v = re.sub(r"^https?://", "", v)
    v = re.sub(r"[^a-z0-9._-]+", "_", v)
    v = re.sub(r"_+", "_", v).strip("_")
    return v or "out"


def _derive_manufacturer_name(input_file: Path) -> str:
    """
    For a filename like 'skf_urls.json' → 'skf' → folder 'skf_data'.
    """
    stem = input_file.stem  # e.g. 'skf_urls'
    if stem.endswith("_urls"):
        stem = stem[:-5]
    return stem or "manufacturer"


def _load_urls(input_file: Path) -> List[str]:
    """
    Accept any of these shapes:
      - {"urls": [...]}
      - {"data": {"urls": [...]}}
      - [...]  (plain list)
    """
    obj: Any = json.loads(input_file.read_text(encoding="utf-8"))

    if isinstance(obj, list):
        return [u for u in obj if isinstance(u, str)]

    if isinstance(obj, dict):
        if isinstance(obj.get("urls"), list):
            return [u for u in obj["urls"] if isinstance(u, str)]
        data = obj.get("data")
        if isinstance(data, dict) and isinstance(data.get("urls"), list):
            return [u for u in data["urls"] if isinstance(u, str)]

    return []


def main():
    parser = argparse.ArgumentParser(
        description="Crawl URLs directly from a mapped list (e.g. skf_urls.json) into <manufacturer>_data/."
    )
    parser.add_argument(
        "urls_json",
        help="Path to mapped URLs JSON (e.g., resources/crawled_data/skf_urls.json)",
    )
    parser.add_argument(
        "--manufacturer",
        help="Manufacturer name for output folder (default is derived from the input filename)",
    )
    parser.add_argument(
        "--cap",
        type=int,
        default=5,
        help="Max number of URLs to process (default: 5)",
    )
    parser.add_argument(
        "--extract",
        help="Optional Firecrawl extract preset/mode (passed through to the client)",
        default=None,
    )
    args = parser.parse_args()

    input_file = Path(args.urls_json)
    if not input_file.exists():
        raise FileNotFoundError(f"URLs file not found: {input_file}")

    urls = _load_urls(input_file)
    if not urls:
        print(f"No URLs found in {input_file}")
        return

    # Apply cap (min 0)
    cap = max(0, args.cap or 0)
    urls = urls[:cap]

    # Output directory: resources/crawled_data/<manufacturer>_data
    manufacturer = args.manufacturer or _derive_manufacturer_name(input_file)
    out_root = Path(settings.out_dir)  # typically 'resources/crawled_data'
    out_dir = out_root / f"{manufacturer}_data"
    ensure_dir(out_dir.as_posix())

    client = FirecrawlClient()
    params: Dict[str, Any] = {}
    if args.extract:
        params["extract"] = args.extract

    print(f"Crawling {len(urls)} URL(s) → {out_dir}")
    for i, u in enumerate(urls, start=1):
        try:
            result = client.crawl_urls([u], params=params)[0]  # single page
            slug = _sanitize_for_filename(u)
            out_path = out_dir / f"{slug}.json"

            payload = result.get("result")
            # Extra guard against non-serializable leftovers (shouldn't be needed after normalization)
            if not isinstance(payload, (dict, list, str, int, float, bool)) and payload is not None:
                payload = str(payload)

            write_json(out_path.as_posix(), {"url": u, "data": payload})
            print(f"[{i}/{len(urls)}] OK  {u}  →  {out_path.name}")
            time.sleep(0.1)
        except Exception as e:
            slug = _sanitize_for_filename(u)
            out_path = out_dir / f"{slug}.json"
            write_json(out_path.as_posix(), {"url": u, "error": str(e)})
            print(f"[{i}/{len(urls)}] ERR {u}: {e}")

if __name__ == "__main__":
    main()