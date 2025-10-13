# EDM-Produkt-Texter  
Extrahiert Produktdaten und erstellt daraus Texte.

# Projektstruktur  

- gui | derzeit irrelevant, zukünftige Erweiterungsmöglichkeit |

- resources                             | Ressourcendateien |  
   - manufacturer_data                  | JSON- und Excel-Dateien mit Herstellerdaten |  
    - manufacturers.json                | Enthält die URLs zu den Herstellerseiten |

    - product_data                      | JSON- und Excel-Dateien mit Produktdaten |

    - crawled_data                      | Durch Scraping erfasste Daten |  
        - manufacturer url_urls.json    | Enthält alle gescrapten URLs einer Herstellerseite |  
        - artikelnr_data.json           | Enthält die gescrapten Daten eines Produkts |

    - templates                         | Strukturvorlagen für die Produkttexte |  
        - example_texts                 | Fertige Beispieltexte zur Orientierung |  
        - specific_rules                | Produkttyp- oder herstellerspezifische Regeln |

- src                                   | Python-Code |  
    - firecrawl_client                  | |  
        - __init__.py                   | Leere __init__-Dateien, damit „src“ ein Paket ist |  
        - client.py                     | Minimaler Firecrawl-API-Client (map + crawl) |
    
    - pipelines                         | |  
        - crawl_products.py             | CLI: Matches → <artikelnr>_data.json |  
        - map_urls.py                   | CLI: Hersteller → <manufacturer>_urls.json |

    - utils                             | |  
        - __init__.py                   | Leere __init__-Dateien, damit „src“ ein Paket ist |  
        - config.py                     | Lädt .env und Standardwerte |  
        - io.py                         | Datei-IO-Helfer |

- styles                                | derzeit irrelevant, zukünftige Erweiterungsmöglichkeit |

- .env                                  | Enthält API-Schlüssel |  
- .gitignore                            | In Git ignorierte Dateien |  
- README.md                             | Diese Datei |  
- requirements.txt                      | Python-Abhängigkeiten |  
- run_project.py                        | Haupt-Starter (CLI) |

# Crawling  

Um das Crawlen von URLs zu starten, führe Folgendes aus:

    pip install -r requirements.txt

und dann entweder

    python run_project.py map resources/manufacturer_data/manufacturers.json --max-depth 3

für alle Hersteller oder

    python run_project.py map https://manufacturer.example.com --max-depth 3

für eine bestimmte Herstellerseite.

Um das Crawlen von Produktdaten zu starten, führe aus:

    -

# Struktur der Produkttexte  

Siehe Regelwerk_Produkttext_Allgemein.md.
