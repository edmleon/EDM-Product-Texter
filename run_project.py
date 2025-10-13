#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Ensure project root on sys.path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utils.config import settings
from src.utils.io import ensure_dir
from src.pipelines.map_urls import main as map_main
from src.pipelines.crawl_products import main as crawl_main


def _read_manufacturers_from_json(json_path: Path) -> List[Dict[str, Any]]:
    if not json_path.exists():
        raise FileNotFoundError(f"Manufacturers file not found: {json_path}")
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Expect: {"manufacturers": [ { "name":..., "url":..., "crawled_data_file":... }, ... ]}
    if not isinstance(data, dict) or "manufacturers" not in data or not isinstance(data["manufacturers"], list):
        raise ValueError(
            "Invalid manufacturers JSON. Expected an object with a 'manufacturers' array of objects."
        )

    items = []
    for item in data["manufacturers"]:
        if not isinstance(item, dict):
            continue
        url = item.get("url")
        out_file = item.get("crawled_data_file")
        name = item.get("name")
        if isinstance(url, str) and url.strip():
            entry = {
                "url": url.strip(),
                "out_filename": out_file.strip() if isinstance(out_file, str) and out_file.strip() else None,
                "name": name.strip() if isinstance(name, str) and name.strip() else None,
            }
            items.append(entry)

    if not items:
        raise ValueError("No valid manufacturers found in 'manufacturers' array.")

    return items


def _run_map_for_url(url: str, max_depth: int | None, out_filename: str | None):
    # Build argv for map_urls.py so we reuse its CLI and logic
    argv = ["map_urls.py", url]
    if max_depth is not None:
        argv += ["--max-depth", str(max_depth)]
    if out_filename:
        argv += ["--out-filename", out_filename]
    sys.argv = argv
    return map_main()


def main():
    parser = argparse.ArgumentParser(prog="run_project", description="Firecrawl mapping & crawling launcher")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # MAP
    p_map = sub.add_parser("map", help="Map manufacturer URLs")
    p_map.add_argument(
        "manufacturer_input",
        help="Either a single URL (e.g., https://example.com) OR a JSON path (e.g., resources/manufacturer_data/manufacturers.json)"
    )
    p_map.add_argument("--max-depth", type=int, default=None, help="Depth-like knob (translated to 'limit')")
    p_map.add_argument("--sitemap", choices=["include", "only", "exclude"], default="include",
                       help="Whether to include sitemap links (propagated to map_urls)")
    # (no --out-filename here; it comes from JSON rows)

    # CRAWL
    p_crawl = sub.add_parser("crawl", help="Crawl matched product URLs")
    p_crawl.add_argument("matches_json", help="Path to JSON mapping {artikelnr: url}")
    p_crawl.add_argument("--extract", default=None, help="Optional Firecrawl extract preset")

    args, extra = parser.parse_known_args()
    ensure_dir(settings.out_dir)

    if args.cmd == "map":
        inp = args.manufacturer_input
        if inp.lower().endswith(".json"):
            items = _read_manufacturers_from_json((ROOT / inp) if not Path(inp).is_absolute() else Path(inp))
            for it in items:
                print(f"\n=== Mapping manufacturer: {it.get('name') or it['url']} ===")
                _run_map_for_url(it["url"], args.max_depth, it.get("out_filename"))
        else:
            # Single URL path (no custom filename)
            _run_map_for_url(inp, args.max_depth, None)
        return

    if args.cmd == "crawl":
        sys.argv = ["crawl_products.py", args.matches_json] + (["--extract", args.extract] if args.extract else [])
        return crawl_main()

if __name__ == "__main__":
    main()