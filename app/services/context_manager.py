from typing import Optional, Type
from app.services.crawler_interface import CrawlerInterface


class ContextManager:

    def __init__(self):
        self.contexts = {}

    def register_context(self, name: str, context_class: Type[CrawlerInterface]):
        self.contexts[name] = context_class()

    def get_context(self, name: str) -> Optional[CrawlerInterface]:
        return self.contexts.get(name)
