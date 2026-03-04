from dataclasses import dataclass
from datetime import datetime, date
from .objects import TransactionType


@dataclass
class Transaction:
    id: str | None
    created: datetime
    type: TransactionType
    due: date
    description: str
    amount: int
    category: str
