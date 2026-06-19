from uuid import uuid4, UUID

from sqlalchemy import Date, Integer, String, Enum, select, extract, update, desc
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

    recurrence: Mapped[f.Recurrence] = mapped_column(Enum(f.Recurrence))

    contact: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(255))
    notes: Mapped[str] = mapped_column(String)


class FutureRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, future: f.Future) -> None:
        self._session.add(self._to_table(future))
        self._session.commit()

    def get(self, id: str) -> f.Future | None:
        try:
            uuid = UUID(id)
        except ValueError:
            return None

        future = self._session.get(FutureTable, uuid)

        if not future:
            return None

        return self._to_model(future)
    
    def update(self, future: f.Future) -> None:
        stmt = (
            update(FutureTable)
            .where(FutureTable.id == future.id)
            .values(
                status=future.status,
                contact=future.contact,
                amount=future.amount,
                paid=future.paid,
                category=future.category,
                notes=future.notes,
                due=future.due,
            )
        )

        self._session.execute(stmt)
        self._session.commit()

    def all(self) -> list[f.Future]:

        rows = self._session.scalars(
            select(FutureTable)
            .order_by('due')
        ).all()

        return [self._to_model(row) for row in rows]
    
    def search(self, term: str) -> list[f.Future]:
        rows = self._session.scalars(
            select(FutureTable).where(
                    (FutureTable.contact == term) |
                    (FutureTable.amount == term) |
                    (FutureTable.notes == term)
            ).order_by('due')
        ).all()

        return [self._to_model(row) for row in rows]    
    
    def by_month(self, month: int | None, year: int | None) -> list[f.Future]:
        rows = self._session.scalars(
            select(FutureTable).where(
                extract('year', FutureTable.due) == year,
                extract('month', FutureTable.due) == month
            ).order_by(FutureTable.due, desc(FutureTable.kind))
        ).all()

        return [self._to_model(row) for row in rows]
    
    def delete(self, id: str) -> bool:
        try:
            uuid = UUID(id)
        except ValueError:
            return False

        future = self._session.get(FutureTable, uuid)

        if not future:
            return False

        self._session.delete(future)
        self._session.commit()
        return True

    def _to_model(self, row: FutureTable) -> f.Future:
        return f.Future(
            id=row.id,
            kind=row.kind,
            issued=row.issued,
            due=row.due,
            status=row.status,
            amount=row.amount,
            paid=row.paid,
            recurrence=row.recurrence,
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
            recurrence=model.recurrence,
            contact=model.contact,
            category=model.category,
            notes=model.notes,
        )
