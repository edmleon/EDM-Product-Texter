# EDM-Product-Texter
Scrapes data of products and creates texts with it.

# Project Structure

- gui | currently irrelevant, future expansion possibility |

- resources                             | resource files |
   - manufacturer_data                  | json and excel files containing manufacturer data |
    - manufacturers.json                | contains the urls to the manufacturer sites |

    - product_data                      | json and excel files containing product data |

    - crawled_data                      | data aqquired through scraping |
        - manufacturer url_urls.json    | contains all scraped urls of a manufacturer site |
        - artikelnr_data.json           | contains the scraped data of a product |

    - templates                         | structure templates for the product texts |
        - example_texts                 | finished example texts for orientation |

        - specific_rules                | product type or manufacturer specific rules |

- src                                   | python code |
    - firecrawl_client                  | |
        - __init__.py                   | empty __init__ files so 'src' is a package |
        - client.py                     | minimal Firecrawl API client (map + crawl) |
    
    - pipelines                         | |
        - crawl_products.py             | CLI: matches → <artikelnr>_data.json |
        - map_urls.py                   | CLI: manufacturer → <manufacturer>_urls.json |

    - utils                             | |
        - __init__.py                   | empty __init__ files so 'src' is a package |
        - config.py                     | loads .env, defaults |
        - io.py                         | file IO helpers |

- styles                                | currently irrelevant, future expansion possibility |

- .env                                  | contains api keys |
- .gitignore                            | ignored files in git |
- README.md                             | this file |
- requirements.txt                      | python requirements |
- run_project.py                        | root launcher (CLI) |

# Crawling

To start crawling urls run

    pip install -r requirements.txt

and then either

    python run_project.py map resources/manufacturer_data/manufacturers.json --max-depth 3

for all manufacturers, or

    python run_project.py map https://manufacturer.example.com --max-depth 3

for a specific manufacturer site.

To star crawling product data run

    - tbd

# Product Text Structure 

See Regelwerk_Produkttext_Allgemein.md.