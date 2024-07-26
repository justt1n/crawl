# app/routers/crawler.py

from fastapi import APIRouter, Depends, HTTPException
from app.models.context_request import ContextRequest
from app.services.google_sheets import GoogleSheetsService
from app.services.context_manager import ContextManager

router = APIRouter()


def get_google_sheets_service():
    # Replace with actual initialization logic
    return GoogleSheetsService(credentials="your-credentials", spreadsheet_id="your-spreadsheet-id")


def get_context_manager():
    return ContextManager()


@router.post("/crawl/")
def trigger_crawler(
        context_request: ContextRequest,
        google_sheets_service: GoogleSheetsService = Depends(get_google_sheets_service),
        context_manager: ContextManager = Depends(get_context_manager)
):
    try:
        context = context_manager.get_context(context_request.context_name)
        if context is None:
            raise HTTPException(status_code=404, detail="Context not found")

        crawled_data = context.crawl()
        google_sheets_service.save_data(crawled_data)

        return {"message": "Crawler triggered successfully", "data": crawled_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
