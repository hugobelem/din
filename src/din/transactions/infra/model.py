import ulid
from datetime import datetime, date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Date, Enum as SAEnum
from din.shared.infra.db import Base
from din.transactions.core.entity import TransactionType

ulid = ulid.new().str


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(primary_key=True, nullable=False, default=ulid)
    created: Mapped[datetime] = mapped_column(DateTime, index=True)
    type: Mapped[TransactionType] = mapped_column(
        SAEnum(
            TransactionType,
            name='transaction_type',
            native_enum=False,
        ),
        nullable=False,
        index=True,
    )
    due: Mapped[date] = mapped_column(Date, index=True)
    description: Mapped[str] = mapped_column(String, index=True)
    amount: Mapped[int] = mapped_column(Integer, index=True)
    category: Mapped[str] = mapped_column(String, index=True)
