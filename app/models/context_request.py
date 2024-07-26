from pydantic import BaseModel


class ContextRequest(BaseModel):
    context_name: str
