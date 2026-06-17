from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from uuid import UUID

class Kind(StrEnum):
    PAYABLE = 'payable'
    RECEIVABLE = 'receivable'


class Status(StrEnum):
    PAID = 'paid'
    PENDING = 'pending'
    OVERDUE = 'overdue'
    PARTIAL = 'partial'


@dataclass(slots=True, frozen=True)
class Future:
    kind: Kind
    issued: date
    due: date
    status: Status
    amount: int
    paid: int
    contact: str
    category: str
    notes: str
    id: UUID | None = None

    @property
    def outstanding(self) -> int:
        return self.amount - self.paid
