from fastapi import Depends, HTTPException
from app.services.context_manager import ContextManager

context_manager = ContextManager()

def get_context(context_name: str):
    context = context_manager.get_context(context_name)
    if context is None:
        raise HTTPException(status_code=404, detail="Context not found")
    return context