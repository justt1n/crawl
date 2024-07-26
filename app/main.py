from fastapi import FastAPI
from app.routers import crawler
from app.services.context_manager import ContextManager
from app.constants import CRAWL_CONTEXTS

app = FastAPI()

context_manager = ContextManager()

for context in CRAWL_CONTEXTS:
    context_manager.register_context(context, CRAWL_CONTEXTS[context])

app.include_router(crawler.router, prefix="/api", tags=["crawler"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Crawler API"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
