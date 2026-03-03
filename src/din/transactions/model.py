from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Date
from din.infra.db import Base
from datetime import date


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String)
    date: Mapped[date] = mapped_column(Date)
    type: Mapped[str] = mapped_column(String)
