import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()  # loads .env from project root

@dataclass(frozen=True)
class Settings:
    firecrawl_api_key: str = os.getenv("FIRECRAWL_API_KEY", "")
    firecrawl_base_url: str = os.getenv("FIRECRAWL_BASE_URL", "https://api.firecrawl.dev")
    out_dir: str = os.getenv("CRAWLED_DATA_DIR", "resources/crawled_data")

    map_max_depth: int = int(os.getenv("FIRECRAWL_MAP_MAX_DEPTH", "3"))
    crawl_concurrency: int = int(os.getenv("FIRECRAWL_CRAWL_CONCURRENCY", "3"))

settings = Settings()