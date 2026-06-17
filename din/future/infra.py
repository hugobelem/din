from uuid import uuid4, UUID

from sqlalchemy import Date, Integer, String, Enum, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Session

from datetime import date

from din import future as f
from din.settings import DB_BASE


class FutureTable(DB_BASE):
    __tablename__ = 'futures'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    kind: Mapped[f.Kind] = mapped_column(Enum(f.Kind))
    issued: Mapped[date] = mapped_column(Date)
    due: Mapped[date] = mapped_column(Date)

    status: Mapped[f.Status] = mapped_column(Enum(f.Status))

    amount: Mapped[int] = mapped_column(Integer)
    paid: Mapped[int] = mapped_column(Integer)

    contact: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(255))
    notes: Mapped[str] = mapped_column(String)


class FutureRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, future: f.Future) -> None:
        self._session.add(self._to_table(future))
        self._session.commit()

    def all(self) -> list[f.Future]:
        rows = self._session.scalars(select(FutureTable)).all()

        return [self._to_model(row) for row in rows]

    def _to_model(self, row: FutureTable) -> f.Future:
        return f.Future(
            id=row.id,
            kind=row.kind,
            issued=row.issued,
            due=row.due,
            status=row.status,
            amount=row.amount,
            paid=row.paid,
            contact=row.contact,
            category=row.category,
            notes=row.notes,
        )
    
    def _to_table(self, model: f.Future) -> FutureTable:
        return FutureTable(
            id=model.id,
            kind=model.kind,
            issued=model.issued,
            due=model.due,
            status=model.status,
            amount=model.amount,
            paid=model.paid,
            contact=model.contact,
            category=model.category,
            notes=model.notes,
        )
