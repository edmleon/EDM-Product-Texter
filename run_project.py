#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from typing import List

# Ensure project root on sys.path so 'src' is importable when launched from root
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utils.config import settings
from src.utils.io import ensure_dir
from src.pipelines.map_urls import main as map_main
from src.pipelines.crawl_products import main as crawl_main

def _read_manufacturers_from_json(json_path: Path) -> List[str]:
    if not json_path.exists():
        raise FileNotFoundError(f"Manufacturers file not found: {json_path}")
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Accept either {"manufacturers": [...]} or a plain list ["https://...", ...]
    if isinstance(data, dict) and "manufacturers" in data and isinstance(data["manufacturers"], list):
        urls = data["manufacturers"]
    elif isinstance(data, list):
        urls = data
    else:
        raise ValueError(
            "Invalid manufacturers JSON. Use either:\n"
            '{ "manufacturers": ["https://...", "https://..."] }\n'
            "or a plain JSON list: [\"https://...\", \"https://...\"]"
        )

    # Validation
    urls = [u for u in urls if isinstance(u, str) and u.strip()]
    if not urls:
        raise ValueError("No manufacturer URLs found in JSON.")
    return urls


def _run_map_for_url(url: str, max_depth: int | None):
    # Reuse the pipeline’s CLI entrypoint to keep behavior identical
    argv = ["map_urls.py", url]
    if max_depth is not None:
        argv += ["--max-depth", str(max_depth)]
    sys.argv = argv
    return map_main()


def main():
    parser = argparse.ArgumentParser(
        prog="run_project",
        description="Firecrawl mapping & crawling launcher"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # MAP
    p_map = sub.add_parser("map", help="Map manufacturer URLs")
    p_map.add_argument(
        "manufacturer_input",
        help="Either a single URL (e.g., https://example.com) OR a JSON path (e.g., manufacturer_data/manufacturers.json)"
    )
    p_map.add_argument("--max-depth", type=int, default=None, help="Override map depth")

    # CRAWL
    p_crawl = sub.add_parser("crawl", help="Crawl matched product URLs")
    p_crawl.add_argument("matches_json", help="Path to JSON mapping {artikelnr: url}")
    p_crawl.add_argument("--extract", default=None, help="Optional Firecrawl extract preset")

    args, extra = parser.parse_known_args()

    # Make sure output dir exists
    ensure_dir(settings.out_dir)

    if args.cmd == "map":
        inp = args.manufacturer_input
        # If user passed a JSON file, loop through all manufacturers inside
        if inp.lower().endswith(".json"):
            urls = _read_manufacturers_from_json((ROOT / inp) if not Path(inp).is_absolute() else Path(inp))
            for u in urls:
                print(f"\n=== Mapping manufacturer: {u} ===")
                _run_map_for_url(u, args.max_depth)
        else:
            # Treat as a single URL
            _run_map_for_url(inp, args.max_depth)
        return

    if args.cmd == "crawl":
        # Delegate to pipeline CLI (keeps existing behavior)
        sys.argv = ["crawl_products.py", args.matches_json] + (["--extract", args.extract] if args.extract else [])
        return crawl_main()


if __name__ == "__main__":
    main()