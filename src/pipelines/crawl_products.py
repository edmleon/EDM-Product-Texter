#!/usr/bin/env python3
import argparse
import json
from typing import Dict, Any

from src.firecrawl_client.client import FirecrawlClient
from src.utils.io import ensure_dir, write_json
from src.utils.config import settings

def load_matches(path: str) -> Dict[str, str]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Matches file must be a JSON object of {artikelnr: url}")
    for art, url in data.items():
        if not isinstance(art, str) or not isinstance(url, str):
            raise ValueError("All artikelnr and urls must be strings")
    return data

def main():
    parser = argparse.ArgumentParser(description="Crawl matched product URLs and save <artikelnr>_data.json")
    parser.add_argument("matches_json", help="Path to JSON mapping {artikelnr: url}")
    parser.add_argument("--extract", help="Optional Firecrawl extraction mode/preset", default=None)
    args = parser.parse_args()

    matches = load_matches(args.matches_json)
    client = FirecrawlClient()

    ensure_dir(settings.out_dir)

    params: Dict[str, Any] = {}
    if args.extract:
        params["extract"] = args.extract  # adapt to Firecrawl's expected shape

    for artikelnr, url in matches.items():
        try:
            result = client.crawl_urls([url], params=params)[0]
            out_path = f"{settings.out_dir}/{artikelnr}_data.json"
            write_json(out_path, {
                "artikelnr": artikelnr,
                "url": url,
                "data": result["result"]
            })
            print(f"OK  {artikelnr} → {out_path}")
        except Exception as e:
            out_path = f"{settings.out_dir}/{artikelnr}_data.json"
            write_json(out_path, {
                "artikelnr": artikelnr,
                "url": url,
                "error": str(e)
            })
            print(f"ERR {artikelnr}: {e}")

if __name__ == "__main__":
    main()