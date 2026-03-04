from dataclasses import dataclass
from datetime import date
from din.transactions.core.entity import TransactionType

@dataclass
class TransactionUpdate:
    type: TransactionType | None
    due: date | None = None
    description: str | None = None
    amount: int | None = None
    category: str | None = None
