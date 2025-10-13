import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

def _clean(s: Optional[str]) -> str:
    return (s or "").strip()

@dataclass
class ManufacturerEntry:
    name: str
    url: str
    out_file: Optional[str]  # e.g., "skf_urls.json"
    db_supplier_name: str    # exact match target for CSV "Lieferant" (if not empty)
    db_manufacturer_name: str# exact match target for CSV "Hersteller" (if not empty)

class ManufacturerIndex:
    """
    Exact manufacturer resolution:
      - If entry.database_supplier_name is non-empty, require CSV.Lieferant == that exact string.
      - If entry.database_manufacturer_name is non-empty, require CSV.Hersteller == that exact string.
      - Empty fields are ignored (they do not cause a miss).
    """
    def __init__(self, manufacturers_json: Path):
        raw = json.loads(Path(manufacturers_json).read_text(encoding="utf-8"))
        arr = raw.get("manufacturers") if isinstance(raw, dict) else None
        if not isinstance(arr, list):
            raise ValueError("manufacturers.json must contain { 'manufacturers': [...] }")

        self.entries: List[ManufacturerEntry] = []
        for m in arr:
            if not isinstance(m, dict):
                continue
            self.entries.append(
                ManufacturerEntry(
                    name=_clean(m.get("name")) or _clean(m.get("url")) or "unknown",
                    url=_clean(m.get("url")),
                    out_file=_clean(m.get("crawled_data_file")) or None,
                    db_supplier_name=_clean(m.get("database_supplier_name")),
                    db_manufacturer_name=_clean(m.get("database_manufacturer_name")),
                )
            )

    def resolve(self, csv_lieferant: str, csv_hersteller: str) -> Optional[ManufacturerEntry]:
        csv_lieferant = _clean(csv_lieferant)
        csv_hersteller = _clean(csv_hersteller)

        for e in self.entries:
            # Both criteria must hold if they are set
            if e.db_supplier_name and csv_lieferant != e.db_supplier_name:
                continue
            if e.db_manufacturer_name and csv_hersteller != e.db_manufacturer_name:
                continue
            # If we got here, all non-empty checks passed.
            return e
        return None