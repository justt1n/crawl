from typing import Optional, Type
from app.services.crawler_interface import CrawlerInterface


class ContextManager:
    def __init__(self, context_list=None):
        self.contexts = dict()
        if context_list is not None:
            for context in context_list:
                self.register_context(context, context_list[context])

    def register_context(self, name: str, context_class: Type[CrawlerInterface]):
        self.contexts[name] = context_class

    def get_context(self, name: str) -> Optional[CrawlerInterface]:
        return self.contexts.get(name)
