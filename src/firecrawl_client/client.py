from __future__ import annotations
import json
import time
from typing import Dict, Any, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.utils.config import settings

# NEW: official SDK
try:
    from firecrawl import Firecrawl
except ImportError:
    Firecrawl = None  # fallback to raw HTTP

class FirecrawlClient:
    """
    Prefer the official SDK (firecrawl-py). Falls back to HTTP if SDK missing.
    """
    def __init__(self,
                 api_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 timeout_s: int = 60):
        self.api_key = api_key or settings.firecrawl_api_key
        self.base_url = (base_url or settings.firecrawl_base_url).rstrip("/")
        self.timeout_s = timeout_s

        if not self.api_key:
            raise RuntimeError("FIRECRAWL_API_KEY is missing. Put it in your .env (starts with fc-).")

        self.sdk = Firecrawl(api_key=self.api_key) if Firecrawl else None

        self.session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "edm-product-texter/1.0",
        })

    # ---------- MAP ----------
    def map_site(self, seed_url: str, limit: int = 2000, sitemap: str = "include") -> Dict[str, Any]:
        """
        Use SDK if available: firecrawl.map(url=..., limit=..., sitemap="include")
        Fall back to /v2/map then /map.
        """
        if self.sdk:
            # SDK returns a list or a structured object depending on version.
            res = self.sdk.map(url=seed_url, limit=limit, sitemap=sitemap)
            return {"_source": "sdk", "data": res}
        # Fallback: raw HTTP (try v2 then v1)
        payload = {"url": seed_url, "limit": limit, "sitemap": sitemap}
        try:
            return {"_source": "http-v2", **self._post("/v2/map", payload)}
        except Exception:
            return {"_source": "http-v1", **self._post("/map", payload)}

    # ---------- CRAWL / SCRAPE SINGLE URL ----------
    def crawl_urls(self, urls: List[str], params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        For matched product URLs you usually want page-level content, not a site-wide job.
        We'll use the SDK's 'scrape' for single pages to get content directly.
        If you truly want recursive crawling per product page, swap to start_crawl/get_crawl_status.
        """
        params = params or {}
        out: List[Dict[str, Any]] = []

        if self.sdk:
            for u in urls:
                # Scrape single page; choose formats as needed
                doc = self.sdk.scrape(u, formats=["markdown", "links", "html"])
                out.append({"url": u, "result": doc})
                time.sleep(0.2)
            return out

        # Fallback raw HTTP: try /v2/scrape then /scrape
        for u in urls:
            payload = {"url": u, "formats": ["markdown", "links", "html"]}
            try:
                data = self._post("/v2/scrape", payload)
            except Exception:
                data = self._post("/scrape", payload)
            out.append({"url": u, "result": data})
            time.sleep(0.2)
        return out

    # ---------- helpers ----------
    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        resp = self.session.post(url, data=json.dumps(payload), timeout=self.timeout_s)
        if resp.status_code >= 400:
            raise RuntimeError(f"Firecrawl error {resp.status_code}: {resp.text[:300]}")
        return resp.json()
