from abc import ABC, abstractmethod
from typing import Any, Dict


class CrawlerInterface(ABC):

    @abstractmethod
    def crawl(self) -> Dict[str, Any]:
        pass
