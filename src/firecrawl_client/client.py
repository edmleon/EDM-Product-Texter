from __future__ import annotations
import json
import time
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.utils.config import settings

# Optional BeautifulSoup support (for normalizing non-JSON results)
try:
    from bs4 import BeautifulSoup  # type: ignore
except Exception:
    BeautifulSoup = None  # type: ignore

# Optional Firecrawl SDK (preferred if installed)
try:
    from firecrawl import Firecrawl  # type: ignore
except Exception:
    Firecrawl = None  # type: ignore


class FirecrawlClient:
    """
    Minimal Firecrawl client that prefers the official SDK if available,
    and gracefully falls back to raw HTTP endpoints. It also normalizes
    non-JSON-serializable results (e.g., BeautifulSoup) so you can dump to JSON.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout_s: int = 60,
    ):
        self.api_key = api_key or settings.firecrawl_api_key
        self.base_url = (base_url or settings.firecrawl_base_url).rstrip("/")
        self.timeout_s = timeout_s

        if not self.api_key:
            raise RuntimeError("FIRECRAWL_API_KEY is missing. Put it in your .env (starts with fc-).")

        # Preferred: official SDK
        self.sdk = Firecrawl(api_key=self.api_key) if Firecrawl else None

        # Fallback HTTP session with retries
        self.session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "edm-product-texter/1.0",
            }
        )

    # -------------------- Public API --------------------

    def map_site(self, seed_url: str, limit: int = 2000, sitemap: str = "include") -> Dict[str, Any]:
        """
        Discover a set of URLs from a site.
        SDK: firecrawl.map(url=..., limit=..., sitemap="include" | "only" | "exclude")
        HTTP fallback: try /v2/map then /map with a similar payload.
        """
        if self.sdk:
            res = self.sdk.map(url=seed_url, limit=limit, sitemap=sitemap)
            # Wrap so downstream code can always read under ["data"]
            return {"_source": "sdk", "data": res}

        payload = {"url": seed_url, "limit": limit, "sitemap": sitemap}
        try:
            return {"_source": "http-v2", **self._post("/v2/map", payload)}
        except Exception:
            return {"_source": "http-v1", **self._post("/map", payload)}

    def crawl_urls(self, urls: List[str], params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Scrape/crawl a list of URLs and return normalized JSON-friendly results.
        SDK: firecrawl.scrape(url, formats=[...])
        HTTP fallback: POST /v2/scrape (or /scrape) per URL.
        """
        results: List[Dict[str, Any]] = []
        params = params or {}

        if self.sdk:
            for u in urls:
                # Ask for rich formats; normalize whatever comes back
                doc = self.sdk.scrape(u, formats=["markdown", "links", "html"])
                results.append({"url": u, "result": self._normalize_result(doc)})
                time.sleep(0.2)  # be polite, tune as needed
            return results

        # Raw HTTP fallback
        for u in urls:
            payload = {"url": u, "formats": ["markdown", "links", "html"]}
            # Merge any extra params the caller provided (e.g., extract preset)
            payload.update(params)
            try:
                data = self._post("/v2/scrape", payload)
            except Exception:
                data = self._post("/scrape", payload)
            results.append({"url": u, "result": self._normalize_result(data)})
            time.sleep(0.2)
        return results

    # -------------------- Internals --------------------

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        resp = self.session.post(url, data=json.dumps(payload), timeout=self.timeout_s)
        if resp.status_code >= 400:
            raise RuntimeError(f"Firecrawl error {resp.status_code}: {resp.text[:300]}")
        return resp.json()

    # -------------------- Normalization --------------------

    @staticmethod
    def _is_soup(obj: Any) -> bool:
        if BeautifulSoup is None:
            return False
        # duck-type: BeautifulSoup/Tag-like (prettify + get_text)
        return hasattr(obj, "prettify") and hasattr(obj, "get_text")

    def _normalize_result(self, obj: Any) -> Any:
        """
        Make Firecrawl/SDK results JSON-serializable.
        - Keep dict/list/primitives as-is
        - BeautifulSoup/Tag → {'html': ..., 'text': ...}
        - Pydantic-like → dict via .model_dump() or .dict()
        - Anything else → string fallback
        """
        # Already JSON-friendly
        if isinstance(obj, (dict, list, str, int, float, bool)) or obj is None:
            return obj

        # BeautifulSoup / Tag
        if self._is_soup(obj):
            try:
                html = obj.prettify()
            except Exception:
                html = str(obj)
            try:
                text = obj.get_text(" ", strip=True)
            except Exception:
                text = ""
            return {"html": html, "text": text}

        # Pydantic-like
        for attr in ("model_dump", "dict"):
            if hasattr(obj, attr):
                try:
                    return getattr(obj, attr)()
                except Exception:
                    pass

        # Last resort: stringify
        try:
            json.dumps(obj)  # if this works, return original
            return obj
        except Exception:
            return str(obj)