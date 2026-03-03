import ulid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from din.infra.db import Base
from datetime import datetime


ulid = ulid.new().str


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(primary_key=True, nullable=False, default=ulid)
    description: Mapped[str] = mapped_column(String)
    amount: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String)
    date: Mapped[datetime] = mapped_column(DateTime)
    type: Mapped[str] = mapped_column(String)
