from dataclasses import dataclass
from datetime import datetime, date

from typing import Literal

@dataclass
class Transaction:
    id: str | None
    created: datetime
    type: Literal[1, 2, 3]
    due: date
    description: str
    amount: int
    category: str
