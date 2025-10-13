# EDM-Product-Texter

Scrapes data of products and creates texts with it.

## Project Structure

- gui                                   | currently irrelevant, future expansion possibility |

- resources                             | resource files |
    - crawled_data                      | data aqquired through scraping |
        - manufacturer url_urls.json    | contains all scraped urls of a manufacturer site |
        - artikelnr_data.json           | contains the scraped data of a product |

    - manufacturer_data                 | json and excel files containing manufacturer data |
        - manufacturers.json            | contains the urls to the manufacturer sites |

    - matched_data                      | |
        - match_report.csv              | |
        - matches.json                  | |

    - product_data                      | json and excel files containing product data |

    - templates                         | structure templates for the product texts |
        - example_texts                 | finished example texts for orientation |

        - specific_rules                | product type or manufacturer specific rules |

- src                                   | python code |
    - firecrawl_client                  | connection to the firecrawl api for webscraping |
        - __init__.py                   | empty __init__ files so 'src' is a package |
        - client.py                     | minimal Firecrawl API client (map + crawl) |

    - matching                          | |
        - __init__.py                   | |
        - manufacturer_index.py         | |
        - matchers.py                   | |
        - normalizers.py                | |
    
    - pipelines                         | workflow |
        - crawl_products.py             | CLI: matches → <artikelnr>_data.json |
        - map_urls.py                   | CLI: manufacturer → <manufacturer>_urls.json |

    - utils                             | utilities, e.g. loading settings and variables |
        - __init__.py                   | empty __init__ files so 'src' is a package |
        - config.py                     | loads .env, defaults |
        - io.py                         | file IO helpers |

- styles                                | currently irrelevant, future expansion possibility |

- .env                                  | contains api keys |
- .gitignore                            | ignored files in git |
- README.md                             | this file |
- requirements.txt                      | python requirements |
- run_project.py                        | root launcher (CLI) |

## Run Project

In the following:

- max-depth means the amount of redirects the crawler goes.

- cap is the amount of urls crawled at one time.

For setup run

    pip install -r requirements.txt

to install all required python packages.

To start crawling urls run either

    python run_project.py map resources/manufacturer_data/manufacturers.json --max-depth 3

for all manufacturers, or

    python run_project.py map https://manufacturer.example.com --max-depth 3

for a specific manufacturer site.

To start crawling product data run either

    python run_project.py crawl-list resources/crawled_data/*.json --cap 5 --extract basic

for data directly from the crawled urls without matching, or

    python run_project.py crawl resources/product_data/matches.json --extract basic

for data matched to EDM productnumber (matching doesnt really work yet though).

## Not Working Currently

To start matching products to urls run

    python run_project.py match --products-csv resources/product_data/*.csv

with your designated product csv.

## Product Text Structure

See Regelwerk_Produkttext_Allgemein.md.
