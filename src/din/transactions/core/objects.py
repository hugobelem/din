from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Money:
    amount: int

    def __add__(self, other: "Money") -> "Money":
        return Money(self.amount + other.amount)


class TransactionType(Enum):
    INCOME = 'income'
    EXPENSE = 'expense'
    TRANSFER = 'transfer'
