from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum


class TransactionType(Enum):
    INCOME = 'income'
    EXPENSE = 'expense'
    TRANSFER = 'transfer'


@dataclass
class Transaction:
    id: str | None
    created: datetime
    type: TransactionType
    due: date
    description: str
    amount: int
    category: str
