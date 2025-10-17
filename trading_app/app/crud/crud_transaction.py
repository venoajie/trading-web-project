
# trading_app/app/crud/crud_transaction.py
import uuid
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.portfolio import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate

async def create_transaction(db: AsyncSession, *, transaction_in: TransactionCreate, user_id: uuid.UUID) -> Transaction:
    # Note: In a real app, we would also verify that the portfolio belongs to the user_id.
    db_transaction = Transaction(**transaction_in.model_dump())
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

# Additional CRUD functions (get, get_multi, update, remove) would be added here.