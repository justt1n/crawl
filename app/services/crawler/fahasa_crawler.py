from typing import Any, Dict
from app.services.crawler_interface import CrawlerInterface


class FahasaCrawler(CrawlerInterface):

    def crawl(self) -> Dict[str, Any]:
        # Implement the logic specific to the Fahasa crawler
        data = {
            "url": "http://fahasa.com",
        }
        return data
