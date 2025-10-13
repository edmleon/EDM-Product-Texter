#!/usr/bin/env python3
import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Optional

from src.matching.manufacturer_index import ManufacturerIndex
from src.matching.matchers import URLMatcher, _extract_numbers_and_codes
from src.matching.normalizers import slugify_for_map_filename
from src.utils.config import settings
from src.utils.io import ensure_dir

LIKELY_ID_COLUMNS = [
    "Artikel Bezeichnung 1", "Artikel Bezeichnung 2", "Artikel Bezeichnung 3",
    "Lieferant", "Hersteller", "Lief. Artikelnr",
    "Lief. Artikel Bezeichnung 1", "Lief. Artikel Bezeichnung 2", "Lief. Artikel Bezeichnung 3",
]

def load_manu_urls(resources_crawled_data: Path, manufacturers_json: Path) -> Dict[str, List[str]]:
    idx = ManufacturerIndex(manufacturers_json)
    manu_to_urls: Dict[str, List[str]] = {}
    for entry in idx.entries:
        filename = entry.out_file or f"{slugify_for_map_filename(entry.url)}_urls.json"
        fp = resources_crawled_data / filename
        if not fp.exists():
            continue
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
            urls = data.get("urls") if isinstance(data, dict) else []
            urls = [u for u in urls if isinstance(u, str)]
            manu_to_urls[entry.name] = urls
        except Exception:
            continue
    return manu_to_urls

def iter_products(csv_path: Path, col_artikelnr: str, col_name: str, col_name2: str, col_supplier: str, col_manufacturer: str) -> Dict[str, Dict]:
    out = {}
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        # Debug: Print header information
        headers = [h.strip() for h in reader.fieldnames or []]
        print(f"CSV Headers: {headers}")
        id_columns = [h for h in headers if h in LIKELY_ID_COLUMNS]
        print(f"ID Columns found: {id_columns}")
        
        row_count = 0
        for row in reader:
            row_count += 1
            if row_count <= 5:  # Print first 5 rows for debugging
                print(f"\nProcessing row {row_count}:")
                print(f"Raw row data: {row}")
            
            artikelnr = (row.get(col_artikelnr) or "").strip()
            if not artikelnr:
                continue
            name = (row.get(col_name) or "").strip()
            name2 = (row.get(col_name2) or "").strip()  # Get second designation
            supplier = (row.get(col_supplier) or "").strip()
            manufacturer = (row.get(col_manufacturer) or "").strip()

            # collect identifiers from known columns + name
            identifiers: List[str] = []
            
            # First, add the primary product code
            main_code = name.strip()  # This is usually the main product code (e.g., 3L250)
            if main_code:
                identifiers.append(main_code)
                # Add variations of the code
                if 'L' in main_code:
                    # Add space-separated version (3L 250 from 3L250)
                    parts = re.match(r'(\d+L)(\d+)', main_code)
                    if parts:
                        identifiers.append(f"{parts.group(1)} {parts.group(2)}")
                        identifiers.append(f"{parts.group(1)}-{parts.group(2)}")
            
            # Then process other columns
            for col in id_columns:
                v = (row.get(col) or "").strip()
                extracted = _extract_numbers_and_codes(v)
                if row_count <= 5:  # Debug output for first 5 rows
                    print(f"Extracted from {col}: {extracted}")
                identifiers.extend(extracted)
                
            # Extract identifiers from both name parts
            name_ids = _extract_numbers_and_codes(name)
            name2_ids = _extract_numbers_and_codes(name2)
            if row_count <= 5:
                print(f"Extracted from name1: {name_ids}")
                print(f"Extracted from name2: {name2_ids}")
            identifiers.extend(name_ids)
            identifiers.extend(name2_ids)

            # Combine both designations and product code for better matching
            full_name = f"{name} {name2}"
            identifiers.extend(_extract_numbers_and_codes(full_name))

            out[artikelnr] = {
                "artikelnr": artikelnr,
                "name": full_name,
                "supplier": supplier,
                "manufacturer": manufacturer,
                "identifiers": list(dict.fromkeys(identifiers)),
            }
            
            if row_count <= 5:
                print(f"Final product entry: {out[artikelnr]}")
                
        print(f"\nTotal rows processed: {row_count}")
    return out

def main():
    parser = argparse.ArgumentParser(description="Match products to manufacturer URLs and emit matches.json")
    parser.add_argument("--manufacturers-json", default="resources/manufacturer_data/manufacturers.json")
    parser.add_argument("--products-csv", default="resources/product_data/50000_Artikel.csv")
    parser.add_argument("--out-matches", default="resources/product_data/matches.json")
    parser.add_argument("--out-report", default="resources/product_data/match_report.csv")
    # CSV columns
    parser.add_argument("--col-artikelnr", default="Artikelnr")
    parser.add_argument("--col-name", default="Artikel Bezeichnung 1")  # Using the first designation
    parser.add_argument("--col-name2", default="Artikel Bezeichnung 2")  # Adding second designation
    parser.add_argument("--col-lieferant", default="Lieferant")
    parser.add_argument("--col-hersteller", default="Hersteller")
    parser.add_argument("--min-score", type=float, default=20.0)  # Lower threshold for testing
    args = parser.parse_args()

    manufacturers_json = Path(args.manufacturers_json)
    products_csv = Path(args.products_csv)
    out_matches = Path(args.out_matches)
    out_report = Path(args.out_report)
    crawled_dir = Path(settings.out_dir)  # resources/crawled_data

    ensure_dir(out_matches.parent)
    ensure_dir(out_report.parent)

    manu_index = ManufacturerIndex(manufacturers_json)
    manu_to_urls = load_manu_urls(crawled_dir, manufacturers_json)
    matcher = URLMatcher()

    products = iter_products(
        products_csv,
        args.col_artikelnr,
        args.col_name,
        args.col_name2,
        args.col_lieferant,
        args.col_hersteller,
    )

    matches: Dict[str, str] = {}
    with out_report.open("w", encoding="utf-8", newline="") as rf:
        from csv import writer as csv_writer
        w = csv_writer(rf, delimiter=";")
        w.writerow(["artikelnr", "resolved_manufacturer", "candidate_count", "chosen_url", "score"])

        for artikelnr, p in products.items():
            entry = manu_index.resolve(p["supplier"], p["manufacturer"])
            if not entry:
                w.writerow([artikelnr, "", 0, "", ""])
                continue

            urls = manu_to_urls.get(entry.name, [])
            if not urls:
                w.writerow([artikelnr, entry.name, 0, "", ""])
                continue

            # NO artikelNr in matching:
            best_url, best_score = matcher.best(
                name=p["name"],
                identifiers=p["identifiers"],
                urls=urls,
            )

            if best_url and best_score >= args.min_score:
                matches[artikelnr] = best_url
                w.writerow([artikelnr, entry.name, len(urls), best_url, f"{best_score:.1f}"])
            else:
                w.writerow([artikelnr, entry.name, len(urls), "", f"{best_score:.1f}"])

    out_matches.write_text(json.dumps(matches, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Matched {len(matches)} products → {out_matches}")

if __name__ == "__main__":
    main()