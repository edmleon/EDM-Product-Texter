# EDM-Produkt-Texter  

Extrahiert Produktdaten und erstellt daraus Texte.

## Projektstruktur  

- gui                                   | derzeit irrelevant, zukünftige Erweiterungsmöglichkeit |

- resources                             | Ressourcendateien |  
    - crawled_data                      | Durch Scraping erfasste Daten |  
        - manufacturer url_urls.json    | Enthält alle gescrapten URLs einer Herstellerseite |  
        - artikelnr_data.json           | Enthält die gescrapten Daten eines Produkts |

    - manufacturer_data                 | JSON- und Excel-Dateien mit Herstellerdaten |  
        - manufacturers.json            | Enthält die URLs zu den Herstellerseiten |

    - matched_data                      | |  
        - match_report.csv              | |  
        - matches.json                  | |

    - product_data                      | JSON- und Excel-Dateien mit Produktdaten |

    - templates                         | Strukturvorlagen für die Produkttexte |  
        - example_texts                 | Fertige Beispieltexte zur Orientierung |  
        - specific_rules                | Produkttyp- oder herstellerspezifische Regeln |

- src                                   | Python-Code |  
    - firecrawl_client                  | Verbindung zur Firecrawl-API für Webscraping |  
        - __init__.py                   | Leere __init__-Dateien, damit „src“ ein Paket ist |  
        - client.py                     | Minimaler Firecrawl-API-Client (map + crawl) |

    - matching                          | |  
        - __init__.py                   | |  
        - manufacturer_index.py         | |  
        - matchers.py                   | |  
        - normalizers.py                | |
    
    - pipelines                         | Workflow |  
        - crawl_products.py             | CLI: Matches → <artikelnr>_data.json |  
        - map_urls.py                   | CLI: Hersteller → <manufacturer>_urls.json |

    - utils                             | Dienstprogramme, z. B. zum Laden von Einstellungen und Variablen |  
        - __init__.py                   | Leere __init__-Dateien, damit „src“ ein Paket ist |  
        - config.py                     | Lädt .env und Standardwerte |  
        - io.py                         | Datei-IO-Helfer |

- styles                                | derzeit irrelevant, zukünftige Erweiterungsmöglichkeit |

- .env                                  | Enthält API-Schlüssel |  
- .gitignore                            | In Git ignorierte Dateien |  
- README.md                             | Diese Datei |  
- requirements.txt                      | Python-Abhängigkeiten |  
- run_project.py                        | Haupt-Starter (CLI) |

## Projekt ausführen  

Im Folgenden gilt:

- *max-depth* bezeichnet die Anzahl der Weiterleitungen, die der Crawler verfolgt.  
- *cap* gibt an, wie viele URLs gleichzeitig gecrawlt werden.

Für die Einrichtung führe aus:

```bash
pip install -r requirements.txt
```

um alle benötigten Python-Pakete zu installieren.

Zum Starten des URL-Crawlings führe entweder aus:

```bash
python run_project.py map resources/manufacturer_data/manufacturers.json --max-depth 3
```

für alle Hersteller oder:

```bash
python run_project.py map https://manufacturer.example.com --max-depth 3
```

für eine bestimmte Herstellerseite.

Zum Starten des Produktdaten-Crawlings führe entweder aus:

```bash
python run_project.py crawl-list resources/crawled_data/*.json --cap 5 --extract basic
```

für Daten direkt von den gecrawlten URLs (ohne Matching), oder:

```bash
python run_project.py crawl resources/product_data/matches.json --extract basic
```

für Daten, die mit EDM-Produktnummern abgeglichen werden (Matching funktioniert derzeit jedoch noch nicht vollständig).

## Aktuell nicht funktionsfähig  

Zum Starten des Matchings zwischen Produkten und URLs führe aus:

```bash
python run_project.py match --products-csv resources/product_data/*.csv
```

unter Verwendung deiner gewünschten Produkt-CSV-Datei.

## Struktur der Produkttexte  

Siehe **Regelwerk_Produkttext_Allgemein.md**.
