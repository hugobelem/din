import ulid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from din.infra.db import Base
from datetime import datetime
from typing import Literal

ulid = ulid.new().str


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(primary_key=True, nullable=False, default=ulid)
    description: Mapped[str] = mapped_column(String, index=True)
    amount: Mapped[int] = mapped_column(Integer, index=True)
    category: Mapped[str] = mapped_column(String, index=True)
    date: Mapped[datetime] = mapped_column(DateTime, index=True)
    type: Mapped[Literal[1, 2, 3]] = mapped_column(Integer, index=True)
