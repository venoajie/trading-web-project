
# trading_app/app/models/conversation.py
import uuid
import datetime
from sqlalchemy import ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.db.base_class import Base

class AIConversation(Base):
    __tablename__ = "ai_conversations"
    __table_args__ = {"schema": "app_data"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("app_data.users.id"), index=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    history: Mapped[dict] = mapped_column(JSONB, nullable=False) # Stores chat history
    summary: Mapped[str | None] = mapped_column(Text)