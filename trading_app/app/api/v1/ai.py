
# trading_app/app/api/v1/ai.py
from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.clients.librarian import librarian_client
from app.db.session import get_db
from app.models.user import User
from app.schemas.ai import AIChatRequest, AIChatResponse
from app.crud import crud_conversation

router = APIRouter()

@router.post("/chat", response_model=AIChatResponse)
async def chat_with_ai(
    request: AIChatRequest = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Proxy endpoint for the Librarian RAG service.
    """
    # 1. Call the external Librarian service
    librarian_response = await librarian_client.query(
        user_id=str(current_user.id),
        prompt=request.prompt
    )

    # 2. Persist the conversation turn in our database for this user
    saved_convo = await crud_conversation.save_conversation(
        db=db,
        user_id=current_user.id,
        prompt=request.prompt,
        response=librarian_response
    )

    # 3. Return the response to the client
    return AIChatResponse(
        answer=librarian_response.get("answer", "No answer found."),
        conversation_id=str(saved_convo.id),
        sources=librarian_response.get("sources", [])
    )