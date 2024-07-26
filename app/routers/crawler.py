# app/routers/crawler.py

from fastapi import APIRouter, Depends, HTTPException
from app.models.context_request import ContextRequest
from app.services.google_sheets import GoogleSheetsService
from app.services.context_manager import ContextManager
from app.constants import CRAWL_CONTEXTS

router = APIRouter()


def get_context_manager():
    context_instances = {name: context() for name, context in CRAWL_CONTEXTS.items()}
    return ContextManager(context_instances)


@router.post("/crawl/")
def trigger_crawler(
        request: ContextRequest,
):
    try:
        google_sheets_service = GoogleSheetsService(sheet_name=request.sheet_name)
        ctx_manager = get_context_manager()
        context = ctx_manager.get_context(request.context_name)
        if context is None:
            raise HTTPException(status_code=404, detail="Context not found")

        crawled_data = context.crawl()
        google_sheets_service.save_data(crawled_data)

        return {"message": "Crawler triggered successfully", "data": crawled_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
