import re
from typing import Iterable, Set

_non_alnum = re.compile(r"[^a-z0-9]+", re.I)
_digit_re = re.compile(r"\d+")

def norm(text: str) -> str:
    if not isinstance(text, str):
        return ""
    t = text.lower().strip()
    t = _non_alnum.sub(" ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def tokens(text: str) -> Set[str]:
    return set(norm(text).split()) if text else set()

def extract_numbers(text: str) -> Set[str]:
    if not text:
        return set()
    return set(_digit_re.findall(text))

def slugify_for_map_filename(url: str) -> str:
    # mirrors your sanitize used for map outputs
    t = url.strip().lower()
    t = re.sub(r"^https?://", "", t)
    t = re.sub(r"[^a-z0-9._-]+", "_", t)
    t = re.sub(r"_+", "_", t).strip("_")
    return t or "out"