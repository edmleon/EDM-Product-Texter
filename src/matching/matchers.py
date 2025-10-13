import re
from typing import Iterable, List, Optional, Tuple

try:
    from rapidfuzz import fuzz
except Exception:
    fuzz = None

_non_alnum = re.compile(r"[^a-z0-9]+")

def _norm(s: str) -> str:
    s = (s or "").lower().strip()
    s = _non_alnum.sub(" ", s)
    return re.sub(r"\s+", " ", s).strip()

def _extract_numbers_and_codes(s: str) -> List[str]:
    """
    Pull out likely identifiers and their components.
    Handles formats like:
    - Simple codes: 3L250, PHG1000
    - Complex codes: 6203-2RSH/C4, LGWA2/0.4
    - Dimensions: 28X47X7
    """
    if not s:
        return []
    s = (s or "").strip()
    result = set()
    
    # Original full alphanumeric blocks
    parts = re.findall(r"[a-zA-Z0-9]{4,}", s)
    result.update(p.lower() for p in parts)
    
    # Product codes with separators (split and whole)
    codes = re.findall(r"[a-zA-Z0-9]+[-/_][a-zA-Z0-9]+(?:[-/_][a-zA-Z0-9]+)*", s)
    for code in codes:
        # Add the whole code
        result.add(code.lower())
        # Add individual components
        components = re.split(r"[-/_]", code)
        result.update(c.lower() for c in components if len(c) >= 2)
    
    # Special formats
    # Bearing series (e.g., 6203, 7205)
    bearing_codes = re.findall(r"\b[0-9]{3,4}\b", s)
    result.update(c for c in bearing_codes if c[0] in "1234567")
    
    # Dimensions (e.g., 28X47X7)
    dims = re.findall(r"\b\d+x\d+x\d+\b", s.lower())
    result.update(dims)
    
    # Product lines (e.g., 3L, 4L, 5L)
    lines = re.findall(r"\b[3-5]l\b", s.lower())
    result.update(lines)
    
    # Special product codes (e.g., LGWA2, LGHP2)
    special = re.findall(r"lg[a-z]{2,4}[0-9]", s.lower())
    result.update(special)
    
    return list(dict.fromkeys(r for r in result))  # unique, order-preserving

def _contains_any(url: str, candidates: Iterable[str]) -> int:
    url = url.lower()
    # Decode URL-encoded characters
    url = re.sub(r'%20', ' ', url)
    url = re.sub(r'%2[fF]', '/', url)
    hits = 0
    
    # Extract product ID from URL if present
    productid_match = re.search(r'productid-([^/]+)$', url)
    product_id = productid_match.group(1).lower() if productid_match else ""
    
    for c in candidates:
        if not c:
            continue
        c = c.lower()
        
        # 1. Direct match in URL or product ID
        if c in url or c in product_id:
            hits += 2  # Higher weight for exact matches
            continue
            
        # 2. Normalized comparison (remove separators)
        v = c.replace("-", "").replace("_", "").replace("/", "").replace(" ", "")
        url_norm = url.replace("-", "").replace("_", "").replace("/", "").replace(" ", "")
        if v and v in url_norm:
            hits += 1
            continue
            
        # 3. Number sequence match (for bearing numbers)
        if c.isdigit() and len(c) >= 3 and c in re.sub(r'[^0-9]', '', url):
            hits += 1
            continue
            
    return hits

class URLMatcher:
    """
    Score URLs against product metadata, without using internal ArtikelNr.
    Heuristics (total ~100 pts):
      - Identifier hits (EAN/MPN/manufacturer code/etc.) → up to 70
      - Token overlap on product name (Jaccard-ish)      → up to 20
      - Fuzzy similarity (RapidFuzz if available)        → up to 10
    """
    def __init__(self, w_ident=70, w_tok=20, w_fuzzy=10):
        self.w_ident = w_ident
        self.w_tok = w_tok
        self.w_fuzzy = w_fuzzy

    def score(self, name: str, identifiers: Iterable[str], url: str) -> float:
        urln = _norm(url)
        # Debug output
        print(f"\nScoring URL: {url}")
        print(f"Product name: {name}")
        
        # 1) identifiers literal presence
        id_list = list(dict.fromkeys(i.lower() for i in identifiers if i))
        print(f"Extracted identifiers: {id_list}")
        
        id_hits = _contains_any(urln, id_list)
        id_score = min(1.0, id_hits / max(1, len(id_list))) if id_list else 0.0
        print(f"Identifier hits: {id_hits}, score: {id_score}")

        # 2) token overlap on name
        nt = set(_norm(name).split()) if name else set()
        ut = set(urln.split())
        print(f"Name tokens: {nt}")
        print(f"URL tokens: {ut}")
        tok_score = (len(nt & ut) / len(nt | ut)) if nt and ut else 0.0
        print(f"Token overlap score: {tok_score}")

        # 3) fuzzy
        if fuzz:
            fuzzy_score = fuzz.partial_ratio(name or "", url or "") / 100.0
        else:
            # fallback: reuse token overlap
            fuzzy_score = tok_score
        print(f"Fuzzy score: {fuzzy_score}")

        final_score = id_score * self.w_ident + tok_score * self.w_tok + fuzzy_score * self.w_fuzzy
        print(f"Final score: {final_score}")
        return final_score

    def best(self, name: str, identifiers: Iterable[str], urls: List[str]) -> Tuple[Optional[str], float]:
        best_url, best_score = None, -1.0
        for u in urls:
            s = self.score(name, identifiers, u)
            if s > best_score:
                best_url, best_score = u, s
        return best_url, best_score