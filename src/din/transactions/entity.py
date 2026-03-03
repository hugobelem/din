from dataclasses import dataclass
from datetime import date


@dataclass
class Transaction:
    id: int
    description: str
    amount: float
    category: str
    date: date
    type: str
