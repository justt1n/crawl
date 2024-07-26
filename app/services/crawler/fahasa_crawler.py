from typing import Any, Dict
from app.services.crawler_interface import CrawlerInterface


class FahasaCrawler(CrawlerInterface):
    def __init__(self):
        pass

    def crawl(self) -> Dict[str, Any]:
        # Implement the logic specific to the Fahasa crawler
        data = {
            "url": "http://fahasa.com",
            "hihi": "haha",
        }
        return data
