
# trading_app/app/schemas/ai.py
from pydantic import BaseModel, Field

class AIChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)
    conversation_id: str | None = None # To continue an existing chat

class AIChatResponse(BaseModel):
    answer: str
    conversation_id: str
    sources: list[dict] = []