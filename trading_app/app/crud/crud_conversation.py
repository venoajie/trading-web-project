
# trading_app/app/crud/crud_conversation.py
import uuid
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.conversation import AIConversation

async def save_conversation(db: AsyncSession, *, user_id: uuid.UUID, prompt: str, response: dict) -> AIConversation:
    # This is a simplified version. A real implementation would append to existing conversations.
    conversation_history = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response.get("answer", "")}
    ]
    
    db_convo = AIConversation(
        user_id=user_id,
        history=conversation_history,
        summary=prompt[:100] # Simple summary
    )
    db.add(db_convo)
    await db.commit()
    await db.refresh(db_convo)
    return db_convo