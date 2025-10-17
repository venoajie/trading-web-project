
# trading_app/app/schemas/transaction.py
import uuid
import datetime
from pydantic import BaseModel, Field
from decimal import Decimal

class TransactionBase(BaseModel):
    instrument_ticker: str = Field(..., max_length=20)
    transaction_type: str = Field(..., pattern="^(BUY|SELL)$") # Enforce BUY or SELL
    quantity: Decimal = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)
    transaction_date: datetime.datetime

class TransactionCreate(TransactionBase):
    portfolio_id: uuid.UUID

class TransactionUpdate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: uuid.UUID
    portfolio_id: uuid.UUID

    class Config:
        from_attributes = True