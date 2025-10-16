
# trading_app/app/models/portfolio.py
import uuid
import datetime
from sqlalchemy import String, ForeignKey, Numeric, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class Portfolio(Base):
    __tablename__ = "portfolios"
    __table_args__ = {"schema": "app_data"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("app_data.users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="portfolios")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="portfolio")

class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = {"schema": "app_data"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("app_data.portfolios.id"), nullable=False)
    instrument_ticker: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(4), nullable=False)  # 'BUY' or 'SELL'
    quantity: Mapped[float] = mapped_column(Numeric(19, 8), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(19, 8), nullable=False)
    transaction_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    portfolio: Mapped["Portfolio"] = relationship(back_populates="transactions")