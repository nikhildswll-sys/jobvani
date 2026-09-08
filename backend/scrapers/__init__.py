"""
JobVani Scrapers Package
Exports department-specific scrapers and master runner.
"""

from .runner import run_all_scrapers, run_department_scraper
from .ssc import scrape_ssc
from .upsc import scrape_upsc
from .railway import scrape_railway
from .defence import scrape_defence
from .police import scrape_police
from .all_india import scrape_all_india

__all__ = [
    "run_all_scrapers",
    "run_department_scraper",
    "scrape_ssc",
    "scrape_upsc",
    "scrape_railway",
    "scrape_defence",
    "scrape_police",
    "scrape_all_india"
]
