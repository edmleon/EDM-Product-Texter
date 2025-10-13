#!/usr/bin/env python3
import argparse
from typing import List
from src.firecrawl_client.client import FirecrawlClient
from src.utils.io import ensure_dir, sanitize_for_filename, write_json
from src.utils.config import settings

def flatten_urls(map_response) -> List[str]:
    urls = set()
    
    # Handle SDK MapData format
    if isinstance(map_response, dict) and "_source" in map_response and map_response["_source"] == "sdk":
        data = map_response.get("data")
        if hasattr(data, "links") and isinstance(data.links, list):
            for link in data.links:
                if hasattr(link, "url") and isinstance(link.url, str):
                    urls.add(link.url)
            return sorted(urls)

    # Handle raw response format
    payload = map_response.get("data") if isinstance(map_response, dict) else map_response

    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, str):
                urls.add(item)
            elif isinstance(item, dict):
                if isinstance(item.get("url"), str):
                    urls.add(item["url"])
                meta = item.get("metadata")
                if isinstance(meta, dict) and isinstance(meta.get("source_url"), str):
                    urls.add(meta["source_url"])

    if isinstance(payload, dict):
        arr = payload.get("urls") or payload.get("data") or []
        if isinstance(arr, list):
            for v in arr:
                if isinstance(v, str):
                    urls.add(v)
                elif isinstance(v, dict):
                    if isinstance(v.get("url"), str):
                        urls.add(v["url"])
                    meta = v.get("metadata")
                    if isinstance(meta, dict) and isinstance(meta.get("source_url"), str):
                        urls.add(meta["source_url"])

        def walk(node):
            if not isinstance(node, dict):
                return
            u = node.get("url")
            if isinstance(u, str):
                urls.add(u)
            for child in node.get("children", []) or node.get("links", []) or []:
                walk(child)
        if "nodes" in payload:
            walk({"children": payload["nodes"]})

    return sorted(urls)

def max_depth_to_limit(md: int | None) -> int:
    """
    Heuristic: translate a 'depth' feeling into an upper bound of discovered URLs.
    Tune as you like.
    """
    if md is None:
        return 2000
    # simple curve: 50 * (md^2) up to 5000
    limit = 50 * (md ** 2)
    return max(100, min(limit, 5000))

def main():
    parser = argparse.ArgumentParser(description="Map manufacturer site to list of URLs")
    parser.add_argument("manufacturer_url", help="Root URL of the manufacturer site (e.g., https://example.com)")
    parser.add_argument("--max-depth", type=int, default=None, help="Depth-like knob (translated to a 'limit')")
    parser.add_argument("--sitemap", choices=["include", "only", "exclude"], default="include",
                        help="Whether to include sitemap links")
    args = parser.parse_args()

    client = FirecrawlClient()

    limit = max_depth_to_limit(args.max_depth)
    # NEW signature: map_site(seed_url, limit=..., sitemap=...)
    res = client.map_site(args.manufacturer_url, limit=limit, sitemap=args.sitemap)
    print(f"DEBUG: API Response: {res}")  # Debug output
    urls = flatten_urls(res)

    ensure_dir(settings.out_dir)
    mfg_slug = sanitize_for_filename(args.manufacturer_url)
    out_path = f"{settings.out_dir}/{mfg_slug}_urls.json"

    write_json(out_path, {"manufacturer_url": args.manufacturer_url, "count": len(urls), "urls": urls})
    print(f"Wrote {len(urls)} URLs → {out_path}")

if __name__ == "__main__":
    main()